import requests
import os
import json
import time

# Credentials
CLIENT_ID = 'X2j9MFeI8m1BlQ'
SECRET_KEY = 'u3AEGdbN2aCzcS4dhK1CKAEwGufxGg'

# Global Variable
doc_id = 0

def create_headers():
    """ Creates request header with authorization token
    Args:
        CLIENT_ID (str): Reddit API Client ID
        SECRET_KEY (str): Reddit API secret token
    Returns:
        headers (dict): headers with authorization token to access reddit API
    """
    # Request Authentication
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    # Retrieve personal password
    with open('password.txt', 'r') as f:
        pw = f.read()

    # Data to request OAuth token
    data = {'grant_type': 'password',
            'username': 'CesardGarrido97',
            'password': pw}

    # Setup header info
    headers = {'User-Agent': 'CovidRedditCrawler/0.0.1'}

    # Send request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # Add authorization token to headers dictionary
    TOKEN = res.json()['access_token']
    #headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    headers['Authorization'] = f'bearer {TOKEN}'

    return headers

def retrieve_subreddit_posts(headers, subreddit='COVID19', filter_flair=None, last_id=None, lang='en', dir='docs'):
    """ Retrieves the text and additional from the specificed subreddit
    Args:
        headers (dict): headers with authorization token to access reddit API.
        subreddit (str): The subreddit where the posts will be retrieved.
        filter_flair (str): flair to filter the posts by.
        last_id (str): The ID of the last post retrieved.
        lang (str): Language of the subreddit.
    Returns:
        json_response (dict): headers with authorization token to access reddit API.
    """
    global doc_id
    # Get last 100 the new posts from the specificed subreddit
    if last_id is None:
        res = requests.get('https://oauth.reddit.com/r/{}/new'.format(subreddit),
                            headers=headers, params={'limit':'100'})
    else:
        res = requests.get('https://oauth.reddit.com/r/{}/new'.format(subreddit),
                        headers=headers, params={'limit':'100', 'after':last_id})

    # Return if reached last posts
    if len(res.json()['data']['children']) < 50:
        return ''

    # Loop over the 100 new posts retrieved
    for post in res.json()['data']['children']:
        try:
            # Retrieve relevant data from Post
            doc = {
                'source' : 'Reddit',
                'subreddit' : post['data']['subreddit'],
                'id':post['kind'] + '_' + post['data']['id'],
                'author':post['data']['author_fullname'],
                'text':post['data']['title'] + ' ' + post['data']['selftext'],
                'url':post['data']['url'],
                'lang':lang
                }
            # Filter by flair if necessary
            if (filter_flair is None) or (post['data']['link_flair_text'].encode('ascii', 'ignore').decode('ascii') == filter_flair):
                # Save post
                with open('{}/REDDIT_{:05d}.json'.format(dir, doc_id), 'w') as fp:
                    json.dump(doc, fp, sort_keys=True, indent=4)
                doc_id += 1
        except:
            pass
            #print('Error retrieving post')

    # Get last id
    new_last_id = doc['id']
    # Delay
    time.sleep(1.5)
    # Return last ID to track
    return new_last_id

def main():
    # Create Authentication headers
    headers = create_headers()

    # ------------------------- ENGLISH SUBREDDITS ---------------------------
    # Define EN Subreddits
    en_subreddits = ['COVID19', 'COVID', 'Coronavirus', 'COVID19positive',
                    'China_Flu', 'COVID19_support', 'CoronavirusCanada',
                    'CanadaCoronavirus', 'CoronavirusUK', 'CoronavirusUs']
    en_last_ids = [None] * len(en_subreddits)

    # ------------------------- SPANISH SUBREDDITS ---------------------------
    # Define ES Subreddits
    es_subreddits = ['noticias_en_espanol', 'covidmx', 'CoronaVirus_Espanol',
                    'argentina', 'Coronaspain']
    es_flair = ['Covid-19', None, None, 'Coronavirus', None]
    es_last_ids = [None] * len(es_subreddits)

    # ------------------------- FRENCH SUBREDDITS ---------------------------
    # Define ES Subreddits
    fr_subreddits = ['france', 'CoronavirusFR', 'CoronavirusFrance', 'Quebec']
    fr_flair = ['Covid-19', None, None, 'Santé']
    fr_last_ids = [None] * len(fr_subreddits)


    # Continous loop
    while (len(en_subreddits) + len(es_subreddits) + len(fr_subreddits)):
        # Retrieve EN Posts
        for i, subreddit in enumerate(en_subreddits):
            en_last_ids[i] = retrieve_subreddit_posts(headers,
                                                      subreddit=subreddit,
                                                      last_id=en_last_ids[i],
                                                      lang='en',
                                                      dir='reddit/en')
        # Retrieve ES Posts
        for i, subreddit in enumerate(es_subreddits):
            es_last_ids[i] = retrieve_subreddit_posts(headers,
                                                      subreddit=subreddit,
                                                      filter_flair=es_flair[i],
                                                      last_id=es_last_ids[i],
                                                      lang='es',
                                                      dir='reddit/es')


        # Retrieve FR Posts
        for i, subreddit in enumerate(fr_subreddits):
            fr_last_ids[i] = retrieve_subreddit_posts(headers,
                                                      subreddit=subreddit,
                                                      filter_flair=fr_flair[i],
                                                      last_id=fr_last_ids[i],
                                                      lang='fr',
                                                      dir='reddit/fr')


        # Delete subreddit if it reaches last post
        for i, ids in enumerate(en_last_ids):
            if ids == '':
                en_last_ids.pop(i)
                en_subreddits.pop(i)

        for i, ids in enumerate(es_last_ids):
            if ids == '':
                es_last_ids.pop(i)
                es_flair.pop(i)
                es_subreddits.pop(i)

        for i, ids in enumerate(fr_last_ids):
            if ids == '':
                fr_last_ids.pop(i)
                fr_flair.pop(i)
                fr_subreddits.pop(i)


        print('Added new posts! - Total Posts: {}'.format(doc_id))
        print('Searching in {} EN, {} ES, {} FR Subreddits'.format(len(en_subreddits),len(es_subreddits),len(fr_subreddits)))


if __name__ == "__main__":
    main()
