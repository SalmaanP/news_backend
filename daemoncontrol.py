#!/usr/bin/env python
 
import sys, time
from daemon import Daemon
import NAS as c
from time import sleep
from datetime import datetime

class MyDaemon(Daemon):
        def run(self):
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
		        sleep(600)

		    except Exception:
		        sleep(1800)
		        continue

 
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-example.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
