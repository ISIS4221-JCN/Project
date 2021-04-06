import requests
import os
import json
import argparse

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")


def create_url():
    query = "covid OR coronavirus OR covid19 -is: retweet -has: images -has: media"
    tweet_fields = "tweet.fields=created_at,lang,geo,entities&expansions=author_id,geo.place_id&user.fields=username"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def tweet_parser(json_response, counter, path):
    tweet_dict = {'source': 'twitter',
                    'id': json_response['id'],
                    'url': 'https://twitter.com/anyuser/status/'+json_response['id'],
                    'lang': json_response['lang'],
                    'date': json_response['created_at'].split('.')[0].replace('T',' '),
                    'author':json_response['author_id'],
                    'text': json_response['text']}
    file = open(path + json_response['lang'] + '/TWITTER_' + str(counter) + '.json', 'w+')
    json.dump(tweet_dict, file, indent=4)
    file.close()
    return json_response['lang']


def main(counters, path):
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAJO4OAEAAAAAZ4vsyUkW68zKBllgu6JqQ%2F9CDXM%3DvJhXoT9phTYwkslDomLzTZ7NWOOPYDYoUzF2jUFNS1MuzTF5s3'
    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    counter = 0
    while json_response['meta']['next_token'] != "":
        url = create_url() + '&next_token=' + json_response['meta']['next_token']
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(url, headers)
        for tweet in json_response['data']:
            if tweet['lang'] in ['es','de','en','it','fr']:     
                counter = counters[tweet['lang']]
                lang = tweet_parser(tweet, counter, path)
                counters[lang] += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--counter_en', type=int, default=0)
    parser.add_argument('--counter_fr', type=int, default=0)
    parser.add_argument('--counter_es', type=int, default=0)
    parser.add_argument('--counter_it', type=int, default=0)
    parser.add_argument('--counter_de', type=int, default=0)
    parser.add_argument('--save_file', type=str, default='/media/juan/Juan/NLP/')
    args = parser.parse_args()
    counters = {'en': args.counter_en, 'fr': args.counter_fr,
        'es': args.counter_es, 'it': args.counter_it, 'de': args.counter_it}
    main(counters, args.save_file)
