import utils
import config as cfg
from gensim import corpora
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))


def build_dictionary(content, DICT_BACKUP):
    """
       A  (Gensim) Dictionary is a map of unique words to unique IDs.

       * Store Dictionary via corpora.dictionary.Dictionary.load/save
    """
    dictionary = []
    DICT_FILE = utils.get_file_path(DICT_BACKUP)
    print('DICT_FILE = {}'.format(DICT_FILE))

    if cfg.DEBUG_ENABLED:
        should_rebuild = True
    else:
        should_rebuild = not utils.try_to_open_file(cfg.DICT_BACKUP)

    if not should_rebuild:
        try:
            print('Loading Dictionary File.')
            # load dict from disk
            dictionary = corpora.dictionary.Dictionary.load(DICT_FILE)
            print('Dictionary Size = {}'.format(len(dictionary)))
        except Exception as exc:
           utils.print_exception_details('Building Dictionary', exc)
    else:
        print('Building Dictionary...')
        dictionary = corpora.Dictionary(content)    # list: (word_id, appearance count)
        # Filter OUT words that:
        #   1. are NOT contained in at least no_below documents
        #   2. are NOT contained in more than 40% of the documents
        # dictionary.filter_extremes(no_below=5, no_above=0.4)
        dictionary.filter_extremes(no_below=3, no_above=0.55)
        # Filter OUT words that are "non meaningful" to topics (stop_words)
        dictionary.filter_tokens(bad_ids=[dictionary.token2id[word] for word in stop_words.intersection(dictionary.values())])
        
        # SAVE the construction
        corpora.dictionary.Dictionary.save(dictionary, DICT_FILE)  # save dict to disk
        print('Dictionary Size = {}'.format(len(dictionary)))
    
    return dictionary

def build_corpus(dictionary, content, CORPUS_BACKUP):
    """
        A (Gensim) Corpus is a "bag of words", which is a histogram map
        for unique and relevant words in a document.

        * Store Corpus (A List) via Pickle
    """
    corpus = []
    corpus_file = utils.get_file_path(CORPUS_BACKUP)

    if cfg.DEBUG_ENABLED:
        should_rebuild = True
    else:
        should_rebuild = not utils.try_to_open_file(cfg.CORPUS_BACKUP)

    if not should_rebuild:
        try:
            print('Loading Corpus File...')
            corpus = corpora.MmCorpus(corpus_file)
        except Exception as exc:
            utils.print_exception_details('Building Corpus', exc)

    else:
        print('Building Corpus...')
        corpus = [dictionary.doc2bow(text) for text in content] # doc-to-bag_of_words
        # SAVE the construction
        corpora.MmCorpus.serialize(corpus_file, corpus) # save corpus to disk

    return corpus