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

def retrieve_subreddit_posts(headers, subreddit='COVID19', filter_flair=None, last_id=None, lang='english'):
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
    # Get last 100 the hot posts from the specificed subreddit
    if last_id is None:
        res = requests.get('https://oauth.reddit.com/r/{}/new'.format(subreddit),
                            headers=headers, params={'limit':'100'})
    else:
        res = requests.get('https://oauth.reddit.com/r/{}/new'.format(subreddit),
                        headers=headers, params={'limit':'100', 'after':last_id})

    #res = requests.get('https://oauth.reddit.com/r/python/hot', headers=headers)

    # Retrieve only relevant info from last 100 posts
    if len(res.json()['data']['children']) == 0:
        return ''

    for post in res.json()['data']['children']:
        try:
            doc = {
                'source' : 'Reddit',
                'subreddit' : post['data']['subreddit'],
                'id':post['kind'] + '_' + post['data']['id'],
                'author':post['data']['author_fullname'],
                'text':post['data']['title'] + ' ' + post['data']['selftext'],
                'url':post['data']['url'],
                'lang':lang
                }
            # Save the post
            with open('docs/REDDIT_{:05d}.json'.format(doc_id), 'w') as fp:
                json.dump(doc, fp, sort_keys=True, indent=4)
            doc_id += 1
        except:
            print('Error retrieving post')

    # Get last id
    new_last_id = doc['id']
    time.sleep(1)
    # Return last ID to track
    return new_last_id

def main():
    headers = create_headers()
    # Define English Subreddits
    eng_subreddits = ['COVID19', 'COVID', 'Coronavirus', 'COVID19positive', 'China_Flu', 'COVID19_support', 'CoronavirusCanada']
    # First iteration
    eng_last_ids = ['', '', '', '', '', '', '']
    for i, subreddit in enumerate(eng_subreddits):
        eng_last_ids[i] = retrieve_subreddit_posts(headers, subreddit=subreddit)

    # Continous loop
    docs_num = len(eng_subreddits)*100
    while True:
        for i, subreddit in enumerate(eng_subreddits):
            # Retrieve english posts
            eng_last_ids[i] = retrieve_subreddit_posts(headers,
                                                       subreddit=subreddit,
                                                       last_id=eng_last_ids[i])

        # Delete subreddit if it reaches last post
        for i, ids in enumerate(eng_last_ids):
            if ids == '':
                eng_last_ids.pop(i)
                eng_subreddits.pop(i)

        docs_num += len(eng_subreddits)*100
        print('Added new posts! - Total Posts: {} (Approx)'.format(docs_num))


if __name__ == "__main__":
    main()
