## Instructions

0. Preparing Wikipedia

0. 1. Using fast.ai scripts

If you want to train your own language model on a Wikipedia in your chosen language, run prepare_wiki.sh. The script will ask for a language and will then download, extract, and prepare the latest version of Wikipedia for the chosen language.

Example command: bash prepare_wiki_fastai.sh

This will create a data folder in this directory and wiki_dumps, wiki_extr, and wiki subfolders. In each subfolder, it will furthermore create a folder LANG where LANG is the language of the Wikipedia. The prepared files are stored in wiki/LANG as train.csv and val.csv to match the format used for text classification datasets. By default, train.csv contains around 100 million tokens and val.csv is 10% the size of train.csv.

0.2 Using gensim

0.3 Using (old) WikiExtractor




# wikipedia_corpus




Selection of script and tools to process a raw wikipedia dump into a text corpus

https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

https://devmount.github.io/GermanWordEmbeddings/

