import numpy as np
import os, json, nltk, random, time
from gensim.parsing.porter import PorterStemmer
from tqdm import tqdm
import string
import concurrent.futures
from nltk.tokenize.casual import TweetTokenizer
import datetime


class Utils:
    def __init__(self, path_prefix, num_workers = 10):
        self.path_prefix = path_prefix
        self.num_workers = num_workers
        self.tweet_tokenizer = TweetTokenizer(preserve_case=False,
                                              reduce_len=True,
                                              strip_handles=True)
        def twitter_date_parser(date):
            return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        def reddit_date_parser(date):
            return datetime.datetime.fromtimestamp(date)
        def news_date_parser(date):
            return datetime.datetime.strptime(date, '%Y-%m-%d')
        self.date_parser = {'tweets': twitter_date_parser,
                            'reddit': reddit_date_parser,
                            'news': news_date_parser}

    def data_loader(self, lang, source,
                    total_data=None,
                    max_size = 400,
                    return_dates = False):
        """ Function to retrieve tweet data in specified language

        Args:
            lang (str): Language to load tweets in [en, es, fr]
            source (str): Source of files to load ['reddit', 'tweets', 'news']
            total_data (int): Total files to load
            max_size (int): Max length of loaded file's string
            return_dates (bool): Return dates or don't

        Returns:
            list: text list
            list: dates
        """
        start = time.time()
        def chunk_loader(path, files_list, return_dates):
            data = []
            dates = []
            for file in files_list:
                with open(os.path.join(path, file), 'r+') as file_str:
                    data_dict = json.load(file_str)
                    text = data_dict['text']
                    if max_size:
                        if len(text.split(' ')) < max_size:
                            data.append(data_dict['text'])
                    else:
                        data.append(data_dict['text'])
                    if return_dates:
                        date = data_dict['date']
                        parsed_date = self.date_parser[source](date)
                        dates.append(parsed_date)
            return data, dates

        path = os.path.join(self.path_prefix, source, lang)
        files_list = os.listdir(path)
        if total_data != None:
            files_list = random.sample(files_list, total_data)
        else:
            total_data = len(files_list)
        lists = np.array_split(files_list, self.num_workers)
        data = []
        dates = []
        print("Starting {} threads to load {} documents from {} in {}".format(self.num_workers, total_data, source, lang))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for files_list in lists:
                futures.append(executor.submit(chunk_loader, path, files_list, return_dates))
            for future in concurrent.futures.as_completed(futures):
                data = data + future.result()[0]
                dates = dates + future.result()[1]
        elapsed_time = time.time() - start

        print("Loaded {} files in {:.2f} seconds.".format(len(data), elapsed_time))
        print("Removed {} files becasuse they were too large".format(total_data - len(data)))
        return data, dates

    def preprocessing(self, text,
                        stop_words = None,
                        stemmer = None,
                        tokenizer = None,
                        lemmatizer = None):
        """ Function to apply preprocessing steps to text

        Args:
            text (str): String to preprocess
            stop_words (list): stopwords to remove
            stemmer (nltk.stem): stemmer to be used
            tokenizer (nltk.tokenize): tokenizer to be used


        Returns:
            str: Preprocessed string
        """
        # Stems text
        if stemmer:
            text = stemmer.stem(text)

        # Removes stopwords
        if tokenizer:
            text = tokenizer.tokenize(text)

        # Converts to lowercase
        text = "".join([char.lower() for char in text if char not in string.punctuation])

        # Lemmatizes text
        relevant_words=[]
        for word in text:
            if word not in stop_words:
                relevant_words.append(word)

        text = relevant_words
        # Returns preprocessed text
        return text

    def tagged_data_loader(self, file_names, source, lang):
        """ Returns text of specified file names

        Args:
            file_names (list): Name of files to be loaded
            source (str): Source to look for the files
            lang (str): Language in which the names will be loaded

        Returns:
            list: tweets list
        """
        start = time.time()
        def chunk_loader(path, files_list):
            data = []
            names = []
            for file in files_list:
                with open(os.path.join(path, file), 'r+') as file_str:
                    names.append(file)
                    data_dict = json.load(file_str)
                    text = data_dict['text']
                    data.append(data_dict['text'])
            return data, names

        lists = np.array_split(file_names, self.num_workers)
        path = os.path.join(self.path_prefix, source, lang)
        data = []
        names = []
        print("Starting {} threads to load {} documents from {} in {}".format(self.num_workers, len(file_names), source, lang))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for files_list in lists:
                futures.append(executor.submit(chunk_loader, path, files_list))
            for future in concurrent.futures.as_completed(futures):
                data = data + future.result()[0]
                names = names + future.result()[1]
        elapsed_time = time.time() - start
        print("Loaded {} files in {:.2f} seconds.".format(len(data), elapsed_time))
        return data, names
