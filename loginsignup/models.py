import subprocess
import sys
from datetime import datetime

from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@python_2_unicode_compatible
class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, default='')
    city = models.CharField(max_length=30, default='')
    state = models.CharField(max_length=30, default='')
    country = models.CharField(max_length=30, default='')
    reg_date = models.DateTimeField(default=datetime.now, blank=True)
    email_confirmed = models.BooleanField(default=False)
    blood_group = models.CharField(max_length=2, default='')

    def __str__(self):
        return self.user.username

    def was_reg_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.reg_date <= now

    was_reg_recently.admin_order_field = 'reg_date'
    was_reg_recently.boolean = True
    was_reg_recently.short_description = 'Registered recently?'


# create and save donor object, after saving user object
def create_profile(sender, **kwargs):
    if kwargs['created']:
        logger.error('Donor creation trigger!')
        user_profile = Donor.objects.create(user=kwargs['instance'])


'''
signal trigger
Specifying sender limits the receiver
to just post_save signals sent for saves of that particular model.
'''
post_save.connect(create_profile, sender=User)


# spawn subprocess to trigger tweepy
# output of subprocess DOES NOT log to the console.
def tweepy_tester(sender, **kwargs):
    if kwargs['created']:
        logger.error('tweepy trigger-start!')
        p = subprocess.Popen([sys.executable, "/Users/viseshprasad/PycharmProjects/Blood_e_Merry/loginsignup/threadtest.py"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        logger.error('tweepy trigger-over!')


# use post_save to trigger tweepy later
# post_save.connect(tweepy_tester, sender=User)
