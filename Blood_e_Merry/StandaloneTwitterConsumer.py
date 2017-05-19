import json

import sys

from psycopg2._psycopg import ProgrammingError
from twilio.rest import TwilioRestClient
import tweepy
import time
import _datetime
from pymongo import MongoClient
import threading
from Blood_e_Merry import bemconstants
import psycopg2

twitter_auth = tweepy.OAuthHandler("Eug8CUA36W1QSxQiARfVR9jAQ", "p24M9jwx9BGLKCi5yxGbIKzBG4sCtmVpO5RzNzmQiCa60dd0KR")
twitter_auth.set_access_token("847427862021812224-TPX5Tyq0EsLIkKU3nDyhSzsALejM6bv",
                              "WPkWhmY2E8Fyf71DJOih4KNkvQjuX1HvlaFtxxyt5l0K9")

twitter_api = tweepy.API(twitter_auth)
pgres_conn = psycopg2.connect("dbname='{}' user='{}' password='{}'".format(bemconstants.pgre_db, bemconstants.pgre_user
                                                                           , bemconstants.pgre_pwd))


class MyTweetStreamListener(tweepy.StreamListener):
    def __init__(self):
        super(MyTweetStreamListener, self).__init__()
        self.mongo_client = MongoClient(host=bemconstants.mongo_host)
        self.sample_db = self.mongo_client[bemconstants.mongo_db]
        self.sample_coll = self.sample_db[bemconstants.mongo_db_collection]
        print('Initialized Twitter Streamer thread....')

    def on_disconnect(self, notice):
        print("Disconnecting...{}".format(notice))

    def on_error(self, status_code):
        if status_code == 420:
            print("Error code 420! Stopping streaming!!!!!!!")
            return False
        elif status_code == 123:
            print('Twitter Streaming Stopping.....')
            return False

    def on_data(self, raw_data):
        print("RAW TWEET :{}".format(raw_data))
        json_data = json.loads(raw_data)
        #        print(raw_data)
        if 'created_at' in json_data:
            json_dict = self.get_json_dict(json_data)
            self.insert_into_mongo(json_dict)
        print("Inserted new tweet......")

    def insert_into_mongo(self, json_dict):
        self.sample_coll.insert_one(json_dict)

    @staticmethod
    def get_json_dict(json_data):
        return TwitterInfo(json_data["created_at"],
                           json_data["id_str"],
                           json_data["text"],
                           json_data["source"],
                           json_data["user"]['location'],
                           json_data["user"]['id_str'],
                           json_data["user"]['name'],
                           json_data["user"]['screen_name'],
                           json_data["user"]['lang'],
                           json_data["geo"],
                           json_data["coordinates"],
                           json_data["place"],
                           json_data["entities"]["hashtags"],
                           json_data["lang"],
                           json_data["filter_level"],
                           json_data["timestamp_ms"],
                           json_data["user"]["screen_name"],
                           is_expired=False).__dict__


class TwitterInfo:
    def __init__(self, created_at, id_str, text, source, user_location, user_id, user_name, user_screenname, user_lang,
                 geo, coordinates, place, hashtags, lang, filter_level, timestamp_ms, user_scrnname, is_expired):
        self.created_at = created_at
        self.id_str = id_str
        self.text = text
        self.source = source
        self.user_location = user_location
        self.user_id = user_id
        self.user_name = user_name
        self.user_screenname = user_screenname
        self.user_lang = user_lang
        self.geo = geo
        self.coordinates = coordinates
        self.place = place
        self.hashtags = hashtags
        self.lang = lang
        self.filter_level = filter_level
        self.timestamp_ms = timestamp_ms
        self.user_scrnname = user_scrnname
        self.is_expired = is_expired


class TwilioThread(threading.Thread):
    def __init__(self):
        super(TwilioThread, self).__init__()
        self.mongo_client = MongoClient(host=bemconstants.mongo_host)
        self.sample_db = self.mongo_client[bemconstants.mongo_db]
        self.sample_coll = self.sample_db[bemconstants.mongo_db_collection]
        self.twilio_client = TwilioRestClient(bemconstants.twilio_account_sid, bemconstants.twilio_auth_token)
        self.signal = True

    def run(self):
        print('Started Twilio Thread....')
        while self.signal:
            time.sleep(bemconstants.msg_check_seconds)
            print('Checking for new Messages....')
            messages = self.sample_coll.find(bemconstants.query)
            for msg in messages:
                self.send_twilio_sms(msg)
        self.mongo_client.close()
        print('Stopping Twilio Thread...')

    def send_twilio_sms(self, msg):
        try:
            cur = pgres_conn.cursor()
            city = "N/A"
            quer_city = '%'
            if msg['place'] is not None and msg['place'] != '':
                city = msg['place']['full_name'].split(',')[0].strip()
                quer_city = city

            print("USER LOCATION IS {}".format(city))
            cur.execute(bemconstants.pgres_query.format(quer_city.lower()))
            user_rows = cur.fetchall()

            # for now with Twilio free API we can only send messages to registered numbers and not any number
            # so for nor using dummy for loop for al the users that match the location criteria.
            cell_num='0'
            for user in user_rows:
                print('User info : {}'.format(user[1]))
                cell_num = user[1].replace(' ','').strip()
                if cell_num is not None and cell_num != '' and len(cell_num) == 10:
                    msg_to_send = bemconstants.twilio_msg_template.format(msg['text'], msg["user_name"], msg["user_screenname"],
                                                                          msg["user_screenname"],
                                                                          city)
                    message = self.twilio_client.messages.create(body=msg_to_send,
                                                                 to='+1'+cell_num,
                                                                 from_=bemconstants.twilio_phone_nbr)
                    self.sample_coll.update_one(
                        {"_id": msg['_id']},
                        {'$set': {
                            'is_expired': True
                        }
                        })
                    print('Sent one message to {}::: {}'.format(cell_num, msg['text']))
        except ProgrammingError as e:
            print("Exception in send_twilio_sms method!!! \n"+ str(e))


def main():
    my_stream_listener = MyTweetStreamListener()
    my_stream = tweepy.Stream(auth=twitter_api.auth, listener=my_stream_listener)
    my_stream.filter(track=bemconstants.trackList, async=True, languages=bemconstants.tweet_languages)

    twilio_thread = TwilioThread()
    twilio_thread.start()
    cmd = 'a'

    while cmd != 'stop':
        cmd = input("")

    twilio_thread.signal = False
    # my_stream_listener.on_error(123)
    my_stream.disconnect()


if __name__ == "__main__": main()
