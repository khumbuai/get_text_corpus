import wget
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-y','--years', nargs='+')
parser.add_argument('-l','--lang',default='en',type=str)
args = parser.parse_args()

for item in args.years:

    url = 'http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.' + item + '.' + args.lang + '.shuffled.gz'
    print('Downloading',url.split('/')[-1])
    filename = wget.download(url)
    os.system("gzip -d " + filename)
    os.remove(filename)

