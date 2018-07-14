import wget
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l','--lang')
args = parser.parse_args()

url = 'http://download.wikimedia.org/' + args.lang + 'wiki/latest/' + args.lang + 'wiki-latest-pages-articles.xml.bz2'
print('Download latest ',args.lang + 'wiki dump')
filename = wget.download(url)