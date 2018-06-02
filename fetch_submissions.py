from __future__ import print_function
import praw
import logging
from setup_logger import setup_logger
from prawoauth2 import PrawOAuth2Mini
import secret 
from newspaper import Article
import blacklist

logger = logging.getLogger("Rotating Log")

def get_submissions(subreddit):
    logger.info("Getting submissions from {0}".format(subreddit))
    r = praw.Reddit(user_agent="Samachar Bot for /r/india by /u/sallurocks")
    scopes = {u'edit', u'submit', u'read', u'privatemessages', u'identity', u'history'}
    try:
        oauth_helper = PrawOAuth2Mini(r, app_key=secret.news_app_key,
                                app_secret=secret.news_app_secret,
                                access_token=secret.news_access_token,
                                refresh_token=secret.news_refresh_token, scopes=scopes)
        submission_object = []
        submissions =  r.get_subreddit(subreddit).get_hot(limit=100)
        for submission in submissions:
            if submission.domain.lower() not in blacklist.blocked:
                t = submission_details(submission, subreddit)
                convert2unicode(t)
                submission_object.append(t)
        logger.info("Fetched {0} submissions from {1}".format(len(submission_object), subreddit))
        return submission_object
    except praw.errors.HTTPException as h:
        logger.error('Something went wrong!', exc_info=True)
        sleep(300)
        return []
    except Exception as e:
        logger.error("Something went wrong!", exc_info=True)
        return []

def submission_details(submission, subreddit):

    article = Article(submission.url)
    article.download()
    article.parse()
    article_text = article.text
    article_meta = article.meta_description
    pub_date = article.publish_date
    title = article.title

    submission_object = {'url': submission.url,
                         'permalink': submission.permalink,
                         'reddit_id': submission.id,
                         'domain': submission.domain,
                         'score': int(submission.score),
                         'newspaper_article': article,
                         'article_text': article_text,
                         'article_meta': article_meta,
                         'pub_date': pub_date,
                         'num_comments': submission.num_comments,
                         'title': title,
                         'category': subreddit}

    return submission_object

def convert2unicode(mydict):
    for k, v in mydict.iteritems():
        if isinstance(v, str):
            mydict[k] = unicode(v, errors = 'replace')
        elif isinstance(v, dict):
            convert2unicode(v)
