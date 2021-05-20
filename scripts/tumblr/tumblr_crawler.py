import json, requests, os, time, argparse
from langdetect import detect
from requests_oauthlib import OAuth1
from requests.exceptions import TooManyRedirects, HTTPError
import numpy as np

def get_headers():
    consumer_key = '0VNHqC43yg3cdeqWD2uUkTDEmHyhdOQFdko4TbiCp2aBUSTRKo'
    consumer_secret = 'TMyRodGzK6ugex7EKBo0O4odHx4zuLk46CldZD7WKoQCtqss3d'
    oauth = OAuth1(consumer_key, client_secret=consumer_secret)

def main(args):
    read_ids = []
    counter = 0
    consumer_key = '0VNHqC43yg3cdeqWD2uUkTDEmHyhdOQFdko4TbiCp2aBUSTRKo'
    consumer_secret = 'TMyRodGzK6ugex7EKBo0O4odHx4zuLk46CldZD7WKoQCtqss3d'
    oauth = OAuth1(consumer_key, client_secret=consumer_secret)
    counters = {'en': 0, 'fr': 0, 'es': 0, 'it': 0, 'de': 0}
    while True:
        response = requests.get(
            'https://api.tumblr.com/v2/tagged?tag=covid', auth=oauth
        )
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        for response_line in response.iter_lines():
            json_response = json.loads(response_line)
            print('Response len: ' + str(len(json_response['response'])))
        for index, blog in enumerate(json_response['response']):
            if not(blog['id_string'] in read_ids):
                read_ids.append(blog['id_string'])
                blog_dict  = {'source': 'tumblr',
                            'url': blog['post_url'],
                            'lang': detect(blog['trail'][0]['content_raw']),
                            'date': blog['date'][:-4],
                            'author':blog['blog_name'],
                            'text': blog['trail'][0]['content_raw']}
                if blog_dict['lang'] in ['en', 'fr', 'it', 'es', 'de']:
                    file = open(args.save_file + blog_dict['lang'] +'/TUMBLR_'+str(counters[blog_dict['lang']])+'.json', 'w+')
                    json.dump(blog_dict, file, indent=4)
                    file.close()
                    counters[blog_dict['lang']] = counters[blog_dict['lang']] + 1
                    counter += 1
                    print('saved blog')
                else:
                    print(blog_dict['lang'])
            else:
                print('Failed Read Blog')
        time.sleep(1000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--counter', type=int, default=0)
    parser.add_argument('--save_file', type=str, default='/media/juan/Juan/NLP/')
    args = parser.parse_args()
    main(args)
