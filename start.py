import fetch_submissions
from setup_logger import setup_logger
import summarize
from insert import insert
import time
import random

logger = setup_logger()
sleep = 10*60
categories = ['technology', 'worldnews', 'india', 'science', 'news', 'canada', 'unitedkingdom', 'upliftingnews', 'europe', 'china']

while True:
    random.shuffle(categories)
    for category in categories:

        submissions = fetch_submissions.get_submissions(category)
        for submission in submissions:
            summarized = summarize.summarize(submission)
            if summarized is not None:
                insert(submission, summarized)
            
    logger.info("Sleeping for {0} minutes".format(sleep/60))
    time.sleep(sleep)