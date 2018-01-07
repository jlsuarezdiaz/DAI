# restaurantes/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

from pymongo import MongoClient
import re as regex
import shelve

client = MongoClient()
db = client.test                  # base de datos
restaurants_db = db.restaurants     # colección

class BoroughNY(models.Model):
    MANHATTAN = 'MH'
    BROOKLYN = 'BK'
    QUEENS = 'QS'
    BRONX = 'BX'
    STATEN_ISLAND = 'SI'

    BOROUGH_DICT = {
        MANHATTAN: 'Manhattan',
        BROOKLYN: 'Brooklyn',
        QUEENS: 'Queens',
        BRONX: 'Bronx',
        STATEN_ISLAND: 'Staten Island',
    }

    BOROUGH_CHOICES = []
    for i in BOROUGH_DICT.keys():
        BOROUGH_CHOICES.append((i,BOROUGH_DICT[i]))

#    BOROUGH_CHOICES = [# (MANHATTAN,BOROUGH_DICT[MANHATTAN]) ]
#        (i, BOROUGH_DICT[i]) for i in BOROUGH_DICT.keys()
#    ]


def groupByAndCount(db,attr):
    aggrcount = list(db.aggregate([
        {'$group': {"_id":"$"+attr,"count":{'$sum':1}}}
    ]))

    counts = {}
    for x in aggrcount:
        counts[x["_id"]] = x["count"]
        
#    counts = {}
#    for item in db.find():
#        val = item
#        for i in range(len(attr)):
#            val = val[attr[i]]
#
#        if val not in counts:
#            counts[val] = int(0)
#        else:
#            counts[val] += int(1)
#
    return counts

#class Profile(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    name = models.TextField(max_length=50, blank=True)
#    surname = models.TextField(max_length=50, blank=True)
#    description = models.TextField(max_length=200)
#
#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()