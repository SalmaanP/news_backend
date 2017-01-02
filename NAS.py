# coding=utf-8
from goose import Goose
import smrzr
import praw
from altsummary import summary as alt_summary
from prawoauth2 import PrawOAuth2Mini
import os
import blacklist
from pymongo import MongoClient
from bson import ObjectId
import datetime
from time import sleep


def init():
    client = MongoClient('mongodb://localhost')
    db = client['samacharbot2']

    r = praw.Reddit(user_agent="Samachar Bot for /r/india by /u/sallurocks")
    scopes = {u'edit', u'submit', u'read', u'privatemessages', u'identity', u'history'}
    oauth_helper = PrawOAuth2Mini(r, app_key=os.environ['news_app_key'],
                                  app_secret=os.environ['news_app_secret'],
                                  access_token=os.environ['news_access_token'],
                                  refresh_token=os.environ['news_refresh_token'], scopes=scopes)

    init_object = {'db': db,
                   'reddit': r,
                   'oauth': oauth_helper,
                   'goose': Goose()}

    return init_object


def get_submissions(r, current_subreddit):
    try:
        subreddit = r.get_subreddit(current_subreddit)
        submissions = subreddit.get_hot(limit=100)
        return submissions
    except praw.errors.HTTPException as h:
        print h
        sleep(300)
        main(current_subreddit)


def summarize(url, article_text):
    summarizer_object = summarize_smrzr(url)
    if summarizer_object is "AssertionError":
        summarizer_object = summarize_alt(article_text)
    elif summarizer_object is None:
        return None

    return summarizer_object


def summarize_smrzr(url):
    try:
        summarized_article = smrzr.Summarizer(url)
    except AssertionError:
        return "AssertionError"
    except smrzr.ArticleExtractionFail:
        print "ArticleExtractionFailed"
        return None
    except Exception as e:
        print e
        return None

    keypoints = summarized_article.keypoints
    article_summary = summarized_article.summary

    if len(article_summary) < 10:
        article_summary = " ".join(keypoints)
    if len(article_summary) > 300:
        article_summary = article_summary[:300] + "..."

    polished_summary = "</li><br><li>".join(keypoints)
    polished_summary = "<ul><li>" + polished_summary + "</li></ul>"
    # polished_summary = polished_summary.replace("`", "")
    # polished_summary = polished_summary.replace("#", "\#")
    source = 'SMRZR'

    summarizer_object = {'summary': article_summary,
                         'keypoints': keypoints,
                         'source': source}

    if len(polished_summary) > 150:
        return summarizer_object
    else:
        print "ArticleExtractionFailed"
        return None


def summarize_alt(article_text):
    keypoints = alt_summary(article_text)
    summary = "\n".join(keypoints)
    summary = summary.replace("`", "")
    summary = summary.replace("#", "\#")

    if len(summary) > 300:
        summary = summary[:300] + "..."
    source = 'ALT'

    summarizer_object = {'summary': summary,
                         'keypoints': keypoints,
                         'source': source}

    if len(summary) > 150:
        return summarizer_object
    else:
        return None


def submission_details(submission, g):
    try:
        goose_article = g.extract(url=submission.url)
    except Exception as e:
        print e
        return None
    article_text = goose_article.cleaned_text
    article_meta = goose_article.meta_description
    pub_date = goose_article.publish_date
    title = goose_article.title

    submission_object = {'url': submission.url,
                         'permalink': submission.permalink,
                         'reddit_id': submission.id,
                         'domain': submission.domain,
                         'score': int(submission.score),
                         'goose_article': goose_article,
                         'article_text': article_text,
                         'article_meta': article_meta,
                         'pub_date': pub_date,
                         'num_comments': submission.num_comments,
                         'title': title}

    return submission_object


def insert(collection, submission_object, summarizer_object):
    submission_object.pop('goose_article', None)

    now = datetime.datetime.now()
    summarizer_object['date_added'] = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0)

    insert_object = submission_object.copy()
    insert_object.update(summarizer_object)

    if collection.find({'reddit_id': submission_object.get('reddit_id')}).count() > 0:
        collection.update_one({'reddit_id': submission_object.get('reddit_id')},
                              {"$set": {"score": submission_object.get('score'),
                                        "num_comments": submission_object.get('num_comments')}}, upsert=True)
        print 'updated'
    else:
        collection.insert_one(insert_object)
        print 'inserted'


def main(subreddit):
    init_object = init()
    reddit_object = init_object.get("reddit")

    submissions = get_submissions(reddit_object, subreddit)

    for submission in submissions:
        print submission.domain
        if submission.domain not in blacklist.blocked:

            submission_object = submission_details(submission, init_object.get("goose"))
            if submission_object is None:
                continue

            summarizer_object = summarize(submission_object.get("url"), submission_object.get("article_text"))
            if summarizer_object is not None:
                insert(init_object.get('db')[subreddit], submission_object, summarizer_object)
