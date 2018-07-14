import os
import nltk.data
from nltk.corpus import stopwords
import re
import logging
import sys
import argparse

# configuration

parser = argparse.ArgumentParser(description='Script for preprocessing public corpora')
parser.add_argument('raw', type=str, help='source file/ folder with raw data for corpus creation')
parser.add_argument('target', type=str, help='target file name to store corpus in')
parser.add_argument('-L', '--Lang', default='en', help='language of corpus supported: de, en')
parser.add_argument('-p', '--punctuation', action='store_true', help='remove punctuation tokens')
parser.add_argument('-s', '--stopwords', action='store_true', help='remove stop word tokens')
parser.add_argument('-u', '--umlauts', action='store_true', help='replace german umlauts with their respective digraphs')
parser.add_argument('-l', '--lowercase', action='store_true', help='replace capital letters with lower case')
parser.add_argument('-S', '--Sentenize', action='store_true', help='tokenize to sentences')
parser.add_argument('-v', '--verbose', default='info',help='logging level: info or debug')

#parser.add_argument('-w', '--wordlist', action='store_true', help='')
args = parser.parse_args()

if args.verbose == 'debug':
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO


logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging_level)


class Config:
    punctuation_tokens = ['.', '..', '...', ',', ';', ':', '(', ')', '"', '\'', '[', ']', '{', '}', '?', '!', '-', u'–',
                          '+', '*', '--', '\'\'', '``', "'",'“','”']
    punctuation = '?.!/;:()&+'

cfg = Config()

target = args.target
target += '.' + args.Lang + '.'
if args.punctuation:
    target += 'p'
if args.lowercase:
    target += 'l'
if args.stopwords:
    target += 's'
if args.Sentenize:
    target += 'S'
target += '.corpus'

if args.Lang == 'en':
    sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    stop_words = stopwords.words('english')
elif args.Lang == 'de':
    sentence_detector = nltk.data.load('tokenizers/punkt/german.pickle')
    stop_words = stopwords.words('german')
else:
    logging.warning('Language not supported, using english instead')
    sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    stop_words = stopwords.words('english')



if args.raw.endswith('/'):
    fns = [args.raw + fn for fn in os.listdir(args.raw) if not fn.startswith('.')]
else:
    fns = [args.raw]

num_files = len(fns)


output = open(target, 'a')
for k, fn in enumerate(fns):
    i = 1
    with open(fn, 'r') as infile:
        for line in infile:

            if args.Sentenize:
                sentences = sentence_detector.tokenize(line)
                for sentence in sentences:
                    # get word tokens
                    words = nltk.word_tokenize(sentence)
                    if args.lowercase:
                        words = [x.lower() for x in words]
                    # filter punctuation and stopwords
                    if args.punctuation:
                        words = [x for x in words if x not in cfg.punctuation_tokens]
                        words = [re.sub('[' + cfg.punctuation + ']', '', x) for x in words]
                    if args.stopwords:
                        words = [x for x in words if x not in stop_words]
                    # write one sentence per line in output file, if sentence has more than 1 word
                    if len(words) > 1:
                        output.write(' '.join(words) + '\n')


            else:

                words = nltk.word_tokenize(line)
                if args.lowercase:
                    words = [x.lower() for x in words]
                # filter punctuation and stopwords
                if args.punctuation:
                    words = [x for x in words if x not in cfg.punctuation_tokens]
                    words = [re.sub('[' + cfg.punctuation + ']', '', x) for x in words]
                if args.stopwords:
                    words = [x for x in words if x not in stop_words]
                # write one sentence per line in output file, if sentence has more than 1 word
                if len(words) > 1:
                    output.write(' '.join(words) + '\n')
                        # process each sentence
            if i % 10000 == 0:
                logging.info('file %s of %s : preprocessing sentence %s ',k+1, num_files, i)
            i += 1
output.close()
logging.info('preprocessing finished!')


