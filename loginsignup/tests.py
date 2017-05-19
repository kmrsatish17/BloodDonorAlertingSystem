import logging
import subprocess
import threading
from multiprocessing import Process

import sys
from django.test import TestCase

logger = logging.getLogger(__name__)


# Create your tests here.

def for_thread():
    i = 0
    while True:
        f = open('test.txt', 'a')
        f.write('Tweepy triggered ' + str(i) + '\n')  # python will convert \n to os.linesep
        f.close()  # you can omit in most cases as the destructor will call it
        i += 1


for_thread()
