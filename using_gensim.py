
from gensim.corpora.wikicorpus import extract_pages, filter_wiki, init_to_ignore_interrupt, utils, IGNORED_NAMESPACES
import bz2
from tqdm import tqdm
import multiprocessing
import logging
logger = logging.getLogger(__name__)

path_to_wiki_dump = 'assets/enwiki-20180620-pages-articles.xml.bz2'

filter_namespaces=('0',)
ep = extract_pages(bz2.BZ2File(path_to_wiki_dump), filter_namespaces)
texts = ((title, text, pageid) for title, text, pageid in tqdm(ep))

def process_article(args):
    title = args[0]
    text = filter_wiki(args[1])
    text = utils.to_unicode(text, encoding = 'utf8', errors="strict")
    text = text.replace('\n', ' ')

    pageid = args[2]
    return title, text, pageid

processes = max(1, multiprocessing.cpu_count() - 1)
pool = multiprocessing.Pool(processes, init_to_ignore_interrupt)

def get_texts(texts):
    articles, articles_all = 0, 0
    positions, positions_all = 0, 0
    try:
        # process the corpus in smaller chunks of docs, because multiprocessing.Pool
        # is dumb and would load the entire input into RAM at once...
        for group in utils.chunkize(texts, chunksize=10 * processes, maxsize=1):
            for title, text, pageid in pool.imap(process_article, group):
                #if articles % 1000 == 0:
                #    print(articles)
                articles_all += 1
                # article redirects and short stubs are pruned here
                if any(title.startswith(ignore + ':') for ignore in IGNORED_NAMESPACES):
                    continue
                if len(text) < 500:
                    continue
                articles += 1
                yield text
    except KeyboardInterrupt:
        logger.warning(
            "user terminated iteration over Wikipedia corpus after %i documents with %i positions "
            "(total %i articles, %i positions before pruning articles shorter than %i words)",
            articles, positions, articles_all, positions_all, 50
        )
    else:
        logger.info(
            "finished iterating over Wikipedia corpus of %i documents with %i positions "
            "(total %i articles, %i positions before pruning articles shorter than %i words)",
            articles, positions, articles_all, positions_all, 50
        )
    finally:
        pool.terminate()

gt = get_texts(texts)

tmp_save = 'assets/tmp/'
with open(tmp_save + 'wiki_text_raw.txt','a') as f:
    for text in tqdm(gt):
        f.write(text + '\n')