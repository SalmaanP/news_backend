__author__ = 'salmaan'

import NAS as c
from time import sleep
from datetime import datetime

count = 0
categories = ['technology', 'worldnews', 'india', 'science', 'news', 'canada', 'unitedkingdom', 'upliftingnews', 'europe', 'china']
while True:

    try:
        count += 1
        try:
            for category in categories:
                print "*************"
                print str(datetime.now())
                print "Now aggregating, current category: " + category + " , current count: " + str(count)
                print "*************"
                c.main(category)
                print "*************"
                print str(datetime.now())
                print "Now aggregating, current count: " + str(count)
                print "*************"
            print "Sleeping for 10 minutes"
            sleep(600)
        except Exception as e:
            print e
            sleep(100)
            pass

    except Exception as e:
        print e
        sleep(100)
        continue
