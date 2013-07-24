#!/bin/python

import unicodedata
import time
import ConfigParser
from datetime import datetime

import twitter
from twython import Twython

#Read the config file in a super unsafe way
for line in open('pyBird.cfg'):
    exec('%s = %s' % tuple(line.split('=', 1)))

DATE_FORMAT_STRING =    '%a %b %d %H:%M:%S +0000 %Y'

debug = False

api = twitter.Api(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=TOKEN_KEY,
    access_token_secret=TOKEN_SECRET
)

t = Twython(
    app_key=CONSUMER_KEY,
    app_secret=CONSUMER_SECRET,
    oauth_token=TOKEN_KEY,
    oauth_token_secret=TOKEN_SECRET
)

def uToString(uStr):
    return unicodedata.normalize('NFKD', uStr).encode('ascii','ignore')
    
def dateToDateTime(date):
   return datetime.strptime(date, DATE_FORMAT_STRING) 

def timeElapsed(dateString):
    dt = dateToDateTime(dateString)
    te = datetime.utcnow() - dt
    days = te.seconds / 60 / 60 / 24
    hours = te.seconds / 60 / 60 % 24
    mins = te.seconds / 60 % 60
    secs = te.seconds % 60
    retstr = ''
    if days > 0:
        retstr = str(days) + " days "
    elif hours > 0:
        retstr = str(hours) + " hours "
    elif mins > 0:
        retstr = str(mins) + " minutes "
    else:
        retstr = str(secs) + " seconds "
    retstr = retstr + "ago."
    return retstr

timeline = t.getHomeTimeline() 

def debug(x):
    print '-------------------------------------------'
    for i in range(0, x):
        name = uToString(timeline[i][u'user'][u'name'])
        dt = uToString(timeline[i][u'created_at'])
        te = timeElapsed(dt)
        text = uToString(timeline[i][u'text'])
        print name + ': ' + te 
        print text
        print '-------------------------------------------'
        time.sleep(2)
