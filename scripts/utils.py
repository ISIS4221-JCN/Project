import pandas as pd
import numpy as np
import os, json, nltk, random
from gensim.parsing.porter import PorterStemmer
from tqdm import tqdm

class Utils:
    def __init__(self, path_prefix):
        self.path_prefix = path_prefix
        self.tokenizer = nltk.RegexpTokenizer(r'\w+')
        self.porter_stemmer = PorterStemmer()
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def data_loader(self, lang, source, total_data=None):
        """ Function to retrieve tweet data in specified language

        Args:
            lang (str): Language to load tweets in [en, es, fr]

        Returns:
            list: tweets list
        """
        path = os.path.join(self.path_prefix, source, lang)
        files_list = os.listdir(path)
        data = []
        for file in tqdm(files_list):
            with open(os.path.join(path, file), 'r+') as file_str:
                data_dict = json.load(file_str)
                data.append(data_dict['text'])
        if total_data == None:
            return data
        else:
            return random.sample(data, total_data)

    def preprocessing(self, text,
                            remove_contractions = False,
                            remove_stop_words = False,
                            stemming = False,
                            tonekize = False,
                            lemmatize = False):
        """ Function to apply preprocessing steps to text

        Args:
            text (str): String to preprocess
            remove_contractions (bool): True to apply contractions removal
            remove_stop_words (bool): True to remove stop words
            stemming (bool): True to apply stemming
            tokenize (bool): True to tokenize text
            lemmatize (bool): True to lemmatize

        Returns:
            str: Preprocessed string
        """
        # Converts to lowercase
        text = text.lower()

        # Replace colloquial terms
        if remove_contractions:
            for word in text.split():
                if word in list(contraction_colloq_dict.keys()):
                    text = text.replace(word, contraction_colloq_dict[word])

        # Removes stopwords
        if remove_stop_words:
            text = remove_stopwords(text)

        # Stems text
        if stemming:
            text = self.porter_stemmer.stem_sentence(text)

        # Tokenizes text and removes punctuation
        if tokenize:
            text = self.tokenizer.tokenize(text)

        # Lemmatizes text
        if lemmatize:
            text_lm = []
            for word in text:
               text_lm.append(self.lemmatizer.lemmatize(word))
        text = text_lm

        # Returns preprocessed text
        return text
