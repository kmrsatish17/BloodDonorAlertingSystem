mongo_host = "localhost"
mongo_db = 'bloodemerrydb'
mongo_db_collection = 'tweets_collection'

trackList = ['viseshismybuddybaddy']
trackList = ['bloodneeded']
tweet_languages = ['en']

# twilio
twilio_account_sid = "AC1b737b9c5ac4ab2ca2749f7c4ac84181"  # Your Account SID from www.twilio.com/console
twilio_auth_token = "2f7acc122b5681032d581623bfca480f"  # Your Auth Token from www.twilio.com/console
msg_check_seconds = 5
query = {
    "is_expired": False

}
mobile_num = '+14085641398'
twilio_phone_nbr = '+19803656535'

twilio_msg_template = '\n### Emergency Blood Assistance Needed ### \n' \
                      'Message :{}\n' \
                      'Contact Person: {}\n' \
                      'Twitter name: @{}\n' \
                      'Twitter URL : https://twitter.com/{}\n' \
                      'Location: {}\n' \
                      '\nHelp Save Lives, Create a better World, a stronger Humanity!!'

pgre_user = 'admin'
pgre_db = 'bloodemerry'
pgre_pwd = ''
pgres_query = "SELECT *FROM loginsignup_donor WHERE lower(city) LIKE '{}'"
