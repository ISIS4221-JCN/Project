import os
# File to check all folders and print total number of files
langs = ['es','en','fr']
sources = ['news', 'FakeNews', 'tweets', 'reddit', 'WHO_CDC']

path_prefix = '/media/juan/Juan/NLP/'
counter = 0
for lang in langs:
    for source in sources:
        path = os.path.join(path_prefix, source, lang)
        counter += len(os.listdir(path))
        print('Found {} files in language {} from {}'.format(len(os.listdir(path)), lang, source))
print(counter)
