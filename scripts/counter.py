import os

langs = ['es','en','fr']
sources = ['news', 'FakeNews', 'tweets', 'reddit']

path_prefix = '/media/juan/Juan/NLP/'

for lang in langs:
    for source in sources:
        path = os.path.join(path_prefix, source, lang)
        print('Found {} files in language {} from {}'.format(len(os.listdir(path)), lang, source))
