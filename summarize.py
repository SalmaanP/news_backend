from __future__ import print_function
import smrzr
import logging
from setup_logger import setup_logger
from altsummary import summary as alt_summary

logger = logging.getLogger("Rotating Log")

def summarize(submission):
    logger.debug("Summarizing reddit_id:{0}, category:{1}".format(submission['reddit_id'], submission['category']))
    try:
        summarizer_object = summarize_smrzr(submission.get('url'))
    except AssertionError:
        logger.debug("Assertion Error, Reddit id:{0}, category:{1}".format(submission['reddit_id'], submission['category']))
        summarizer_object = summarize_alt(submission.get('article_text'))
    except smrzr.ArticleExtractionFail:
        logger.error("Article Extraction Fail, Reddit id:{0}, category:{1}".format(submission['reddit_id'], submission['category']))
        return None
    except Exception as e:
        logger.error("Something Went Wrong, Reddit id:{0}, category:{1}".format(submission['reddit_id'], submission['category']), exc_info=True)
        return None

    if summarizer_object is None:
        logger.error("No Summary, Reddit id:{0}, category:{1}".format(submission['reddit_id'], submission['category']), exc_info=True)

    return summarizer_object

def summarize_smrzr(url):

    summarized_article = smrzr.Summarizer(url, 4, 'default', 'newspaper')

    keypoints = summarized_article.keypoints
    article_summary = summarized_article.summary

    if len(article_summary) < 150:
        article_summary = " ".join(keypoints)
    if len(article_summary) > 300:
        article_summary = article_summary[:300] + "..."

    summarizer_object = {'summary': article_summary,
                         'keypoints': keypoints,
                         'source': 'SMRZR'}

    if len(article_summary) > 150:
        return summarizer_object
    else:
        logger.error("No Summary")
        return None 

def summarize_alt(article_text):
    keypoints = alt_summary(article_text)
    summary = "\n".join(keypoints)
    summary = summary.replace("`", "")
    summary = summary.replace("#", "\#")

    if len(summary) > 300:
        summary = summary[:300] + "..."

    summarizer_object = {'summary': summary,
                         'keypoints': keypoints,
                         'source': 'ALT'}

    if len(summary) > 150:
        return summarizer_object
    else:
        return None