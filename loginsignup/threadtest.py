import threading
import time


class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        i = 0
        while True:
            f = open('test.txt', 'a')
            f.write('Tweepy triggered ' + str(i) + '\n')  # python will convert \n to os.linesep
            f.close()  # you can omit in most cases as the destructor will call it
            i += 1

            time.sleep(self.interval)

example = ThreadingExample()
print('Checkpoint')
time.sleep(130000)
print('Bye')
