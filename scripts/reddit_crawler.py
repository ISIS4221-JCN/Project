import requests
import os
import json

# Credentials
CLIENT_ID = 'X2j9MFeI8m1BlQ'
SECRET_KEY = 'u3AEGdbN2aCzcS4dhK1CKAEwGufxGg'

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

def retrieve_subreddit_posts(headers, subreddit=['COVID19']):
    """ Retrieves the text and additional from the specificed subreddit
    Args:
        headers (dict): headers with authorization token to access reddit API
        subreddit (str): The subreddit wanted to be access
    Returns:
        json_response (dict): headers with authorization token to access reddit API
    """
    # Get all the hot posts from the specificed subreddit
    res = requests.get('https://oauth.reddit.com/r/{}/new'.format(subreddit[0]),
          headers=headers, params={'limit':'100'})
    #res = requests.get('https://oauth.reddit.com/r/python/hot', headers=headers)

    # Retrieve only relevant info from last 100 posts
    #print(len(res.json()['data']['children']))
    for post in res.json()['data']['children']:
        #print(post['data'].keys())
        doc = {
            'source' : 'Reddit_'+post['data']['subreddit'],
            'id':post['kind'] + '_' + post['data']['id'],
            'author':post['data']['author_fullname'],
            'text':post['data']['title'] + post['data']['selftext'],
            'url':post['data']['url'],
            'lang':'english'
            }
        print(doc)

def main():
    headers = create_headers()
    retrieve_subreddit_posts(headers)
    #print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
