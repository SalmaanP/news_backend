__author__ = 'salmaan'

import NAS as c
from time import sleep
from datetime import datetime

count = 0
categories = ['india', 'worldnews', 'technology', 'science']
while True:

    try:
        count += 1
        for category in categories:
            print "*************"
            print str(datetime.now())
            print "Awake: Starting now, current category: " + category + " , current count: " + str(count)
            print "*************"
            c.main(category)
            print "*************"
            print str(datetime.now())
            print "Sleeping for 1 hour, current count: " + str(count)
            print "*************"
        sleep(3600)

    except Exception:
        sleep(1800)
        continue
