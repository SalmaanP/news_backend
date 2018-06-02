from __future__ import print_function
from pymongo import MongoClient
import secret 
import datetime
import logging

connection = MongoClient(secret.mongo_url)
db = connection[secret.mongo_db]
logger = logging.getLogger("Rotating Log")

def insert(submission_object, summarizer_object):
    collection = db[submission_object['category']]
    submission_object.pop('newspaper_article', None)

    now = datetime.datetime.now()
    summarizer_object['date_added'] = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0)

    insert_object = submission_object.copy()
    insert_object.update(summarizer_object)
    if collection.find({'reddit_id': submission_object.get('reddit_id')}).count() > 0:
        collection.update_one({'reddit_id': submission_object.get('reddit_id')},
                              {"$set": {"score": submission_object.get('score'),
                                        "num_comments": submission_object.get('num_comments')}}, upsert=True)
        logger.debug("Updated")
    else:
        try:
            collection.insert_one(insert_object)
            logger.debug("Inserted")
        except Exception as e:
            logger.error("Error on inserting {0}, category {1}".format(submission_object['reddit_id'], submission_object['category']), exc_info=True)

