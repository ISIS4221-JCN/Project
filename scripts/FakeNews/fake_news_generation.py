import pandas as pd
import argparse, json, os, random
from tqdm import tqdm
from transformers import pipeline, set_seed


model_dict = {'en': 'gpt2',
              'es': 'datificate/gpt2-small-spanish',
              'fr': 'dbddv01/gpt2-french-small'}

def main(args):
    generator = pipeline('text-generation', model=model_dict[args.lang])
    set_seed(args.seed)
    real_news_names = sorted(os.listdir(args.path + 'OriginalNews/' + args.lang + '/'))
    for counter, file in enumerate(tqdm(real_news_names)):
        with open(args.path + 'OriginalNews/' + args.lang + '/' + file, encoding='utf-8') as opened_file:
            news = json.load(opened_file)
            # base_text = news['title'] + '. ' + news['text'].split('. ')[0] + '. '
            base_text = news['title'] + '. '
            genereated = generator(base_text,  max_length=args.max_length + random.randint(0, 50) , num_return_sequences=1, pad_token_id=50256)
            text = genereated[0]['generated_text']

            fake_news_dict = {'source': 'Generated Fake News',
                        'lang': args.lang,
                        'author': model_dict[args.lang],
                        'text': text}

            file = open(args.path + args.lang+ '/' + 'fake_' + str(counter) + '.json', 'w+', encoding='utf-8')
            json.dump(fake_news_dict, file, indent=4)
            file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='/media/juan/Juan/NLP/FakeNews/')
    parser.add_argument('--counter', type=int, default=0)
    parser.add_argument('--lang', type=str, default='es')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--max_length', type=int, default=300)
    args = parser.parse_args()
    main(args)
