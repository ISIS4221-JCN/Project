import requests
import os
import json
import argparse
from datetime import datetime

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token, lang):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "covid -is: retweet lang: " + lang + " -has: images", "tag": "covid"},
        {"value": "coronavirus -is: retweet lang: " + lang + " -has: images", "tag": "coronavirus"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(headers, set, bearer_token, path):
    counter=0
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?tweet.fields=created_at,lang,geo,entities&expansions=author_id,geo.place_id",
        headers=headers,
        stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweet_dict = {'source': 'twitter',
                        'url': 'https://twitter.com/anyuser/status/'+json_response['data']['id'],
                        'lang': json_response['data']['lang'],
                        'date': json_response['data']['created_at'].split('.')[0].replace('T',' '),
                        'author':json_response['includes']['users'][0]['username'],
                        'text': json_response['data']['text']}
            file = open(path+'twitter'+str(counter)+'.json', 'w+')
            json.dump(tweet_dict, file, indent=4)
            file.close()
            counter += 1

def main(args):
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAJO4OAEAAAAAZ4vsyUkW68zKBllgu6JqQ%2F9CDXM%3DvJhXoT9phTYwkslDomLzTZ7NWOOPYDYoUzF2jUFNS1MuzTF5s3"
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token, args.language)
    get_stream(headers, set, bearer_token, args.save_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', type=str, default='en')
    parser.add_argument('--save_file', type=str, default='/media/juan/Juan/NLP/')
    args = parser.parse_args()
    args.save_file=args.save_file + args.language + '/'
    main(args)
