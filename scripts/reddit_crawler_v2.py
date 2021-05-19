import requests
import os
import json
import time
import praw
import datetime as dt

# Global Variable
doc_num = 223150
post_num = 9000
comment_num = 214150

def retrieve_subreddit_docs(reddit, subreddit_name, filter_flair=None, lang='en', dir='docs'):
    """ Retrieves posts and comments info from the specificed subreddit.
    Args:
        reddit (praw.Reddit): Reddit instance from PRAW.
        subreddit (str): The subreddit where the posts will be retrieved.
        filter_flair (str): flair to filter the posts by.
        last_id (str): The ID of the last post retrieved.
        lang (str): Language of the subreddit.
    Returns:
        json_response (dict): headers with authorization token to access reddit API.
    """
    global doc_num, post_num, comment_num

    # Subreddit instance
    subreddit = reddit.subreddit(subreddit_name)

    # Save docs_id to prevent duplicated docs
    docs_id = []
    # Feeds array
    feeds = []

    # Filter by flairs (if it is the case)
    if filter_flair == None:
        feeds.append(subreddit.new(limit=1000))
        feeds.append(subreddit.top(limit=1000))
        feeds.append(subreddit.hot(limit=1000))
    else:
        feeds.append(subreddit.search(filter_flair, limit=1000))

    # Retrieve posts
    for submissions in feeds:
        for submission in submissions:
            try:
                # Retrieve info from post
                doc = {
                    'source': 'Reddit',
                    'subreddit': subreddit_name,
                    'id': submission.id,
                    'author':submission.author.name,
                    'text': submission.title + ' ' + submission.selftext,
                    'url':submission.url,
                    'date':submission.created,
                    'lang':lang
                    }
            except:
                continue

            # Verify if not duplicated
            if doc['id'] not in docs_id:
                # Add post
                #print(f'{doc_num} Post: {submission.title}')
                docs_id.append(doc['id'])
                post_num += 1
                doc_num += 1
                # Save doc
                with open('{}/REDDIT_{:05d}.json'.format(dir, doc_num), 'w') as fp:
                    json.dump(doc, fp, sort_keys=True, indent=4)
            else:
                continue

            # Retrieve now comments from post
            submission.comments.replace_more(limit=None)
            for comment in submission.comments:
                try:
                    # Retrieve info from comments
                    doc = {
                        'source': 'Reddit',
                        'subreddit': subreddit_name,
                        'id': comment.id,
                        'author':comment.author.name,
                        'text': comment.body,
                        'url':submission.url,
                        'date':comment.created,
                        'lang':lang
                        }
                except:
                    continue

                # Verify that comment has enough words
                if len(comment.body.split()) > 5:
                    # Add comment
                    #print(f'{doc_num}) Comment: {comment.body}')
                    comment_num += 1
                    doc_num += 1
                    # Save post
                    with open('{}/REDDIT_{:05d}.json'.format(dir, doc_num), 'w') as fp:
                        json.dump(doc, fp, sort_keys=True, indent=4)

    print(f'Retrieved new docs...')
    print(f'Total Docs: {doc_num} - ({post_num} Posts and {comment_num} Comments)')

def main():
    """ main method to retrieve posts and comments from reddit."""

    # ----------------------------- CREDENTIALS -------------------------------
    CLIENT_ID = 'X2j9MFeI8m1BlQ'
    SECRET_KEY = 'u3AEGdbN2aCzcS4dhK1CKAEwGufxGg'

    # Personal password
    with open('password.txt', 'r') as f:
        PW = f.read()

    # Reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET_KEY,
                         user_agent='CovidRedditCrawler/0.0.2',
                         username='CesardGarrido97',
                         password=PW)

    # ------------------------- SPANISH SUBREDDITS ---------------------------
    # Define ES Subreddits
    es_subreddits = ['noticias_en_espanol', 'covidmx', 'CoronaVirus_Espanol',
                    'argentina', 'Coronaspain']
    es_flair = ['Covid-19', None, None, 'Coronavirus', None]

    # Retrieve ES Documents
    for i, sub_names in enumerate(es_subreddits):
        # Retrieve subreddit posts
        retrieve_subreddit_docs(reddit, sub_names,
                                 filter_flair=es_flair[i],
                                 lang='es',
                                 dir='reddit/es')

    # ------------------------- FRENCH SUBREDDITS ---------------------------
    # Define FR Subreddits
    fr_subreddits = ['france', 'CoronavirusFR', 'CoronavirusFrance', 'Quebec']
    fr_flair = ['Covid-19', None, None, 'Santé']

    # Retrieve FR Documents
    for i, sub_names in enumerate(fr_subreddits):
        # Retrieve subreddit posts
        retrieve_subreddit_docs(reddit, sub_names,
                                 filter_flair=fr_flair[i],
                                 lang='fr',
                                 dir='reddit/fr')

    # ------------------------- ENGLISH SUBREDDITS ---------------------------
    # Define EN Subreddits
    en_subreddits = ['COVID19', 'COVID', 'Coronavirus', 'COVID19positive',
                    'China_Flu', 'COVID19_support', 'CoronavirusCanada',
                    'CanadaCoronavirus', 'CoronavirusUK', 'CoronavirusUs']
    #en_subreddits = ['COVID19positive', 'COVID19_support', 'China_Flu']

    # Retrieve EN Documents
    for i, sub_names in enumerate(en_subreddits):
        # Retrieve subreddit posts
        retrieve_subreddit_docs(reddit, sub_names,
                                 lang='en',
                                 dir='reddit/en')

if __name__ == "__main__":
    main()
