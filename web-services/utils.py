import os, sys, string, json
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import similarities, corpora, models
# from gensim.test.utils import datapath
# from flask import g # "ENV vars" for flask apps
import config as cfg

lemma = WordNetLemmatizer()
punctuation = set(string.punctuation)
stop_words = set(stopwords.words('english'))


def print_exception_details(what, exc):
    print('Error: {}'.format(what))
    print(exc)

def variable_is_defined(var):
    return 'var' in vars() or 'var' in globals()

def debug_print(what, data):
    print("###################")
    print( what )
    print( data )
    print("###################")

def get_similarity(lda, corpus, q_vec):
    """
    Find related Documents.
    """
    index = similarities.MatrixSimilarity(lda[corpus])
    sims = index[q_vec]
    return sims

def get_file_path(rel_filepath):
    script_path = os.path.abspath(__file__)
    script_dir  = os.path.split(script_path)[0]
    abs_file_path = os.path.join(script_dir, rel_filepath)

    return abs_file_path

def remove_punctuation(text):
    return ''.join(char for char in text if char not in punctuation)

def remove_numbers(text):
    return ''.join(char for char in text if not char.isdigit())

def remove_stop_words(text):
    return ' '.join([word for word in text.split() if word not in stop_words])

def remove_single_characters(text):
    return ' '.join([word for word in text.split() if len(word) > 1])

def lemmatize(text):
    return ' '.join([lemma.lemmatize(word) for word in text.split()])

def pickle_save(PATH, data):
    with open(PATH, "wb") as fp:
        pickle.dump(data, fp)
    fp.close()

def try_to_open_file(path):
    """
    Returns IF it's safe to open file in application.
    TRUE IFF file exists and is openable,
    FALSE otherwise
    """
    # file_exists = True
    try:
        f = open(path)
        f.close()
        return True
    except FileNotFoundError:
        # file_exists = False
        return False
    # return file_exists

# def get_top_topics(limit, topic_details):
#     """
#     Sorts and filters the topic_details from the model to the top (limit)
#     topic details.
#     """
#     topic_details_as_string = str('{}'.format(topic_details))
#     topic_dict = dict()
#     # FIND MAX (3) CONFIDENCE VALUES.
#     # FILL top_three_topics ONLY WITH THE TOPICS 
#     # THAT HAVE THE (3) HIGHEST CONFIDENCE VALUES.

#     # Destructure topic details into a map of confidence-to-TopicDetails
#     for topic_rating in topic_details_as_string.split('+'):
#         confidence = float(topic_rating.split('*')[0])
#         topic = topic_rating.split('*')[1]
#         topic_dict[confidence] = topic_rating

#     # Sort topic_dict dict BY key (confidence)
#     # Now, top_three_topics = first three topic_ratings
#     results = list(sorted(topic_dict.items()))[0:limit]
    # return dict(results)

def get_cleaned_text(text):
    text = text.replace('\n', '')
    text = remove_numbers(text)
    text = remove_stop_words(text)
    text = remove_punctuation(text)
    text = remove_single_characters(text)

    # Lemmatize the Document
    text = lemmatize(text)
    return text

def build_dictionary(content, should_rebuild, DICT_BACKUP):
    """
       A  (Gensim) Dictionary is a map of unique words to unique IDs.

       * Store Dictionary via corpora.dictionary.Dictionary.load/save
    """
    dictionary = []
    DICT_FILE = get_file_path(DICT_BACKUP)
    print('DICT_FILE = {}'.format(DICT_FILE))

    if not should_rebuild:
        try:
            # with open(DICT, "rb") as dict_file:
            #     if dict_file:
            print('Loading Dictionary File.')
            # load dict from disk
            dictionary = corpora.dictionary.Dictionary.load(DICT_FILE)
            print('Dictionary Size = {}'.format(len(dictionary)))
        except Exception as exc:
           print_exception_details('Building Dictionary', exc)
    else:
        print('Building Dictionary...')
        dictionary = corpora.Dictionary(content)    # list: (word_id, appearance count)
        dictionary.filter_extremes(no_below=5, no_above=0.4)
        # SAVE the construction
        corpora.dictionary.Dictionary.save(dictionary, DICT_FILE)  # save dict to disk
        print('Dictionary Size = {}'.format(len(dictionary)))
    
    return dictionary

def build_corpus(dictionary, content, should_rebuild, CORPUS_BACKUP):
    """
        A (Gensim) Corpus is a "bag of words", which is a histogram map
        for unique and relevant words in a document.

        * Store Corpus (A List) via Pickle
    """
    corpus = []
    corpus_file = get_file_path(CORPUS_BACKUP)

    if not should_rebuild:
        try:
            print('Loading Corpus File...')
            corpus = corpora.MmCorpus(corpus_file)
        except Exception as exc:
            print_exception_details('Building Corpus', exc)

    else:
        print('Building Corpus...')
        corpus = [dictionary.doc2bow(text) for text in content] # doc-to-bag_of_words
        # SAVE the construction
        corpora.MmCorpus.serialize(corpus_file, corpus) # save corpus to disk

    return corpus

def model_switch_dict():
    return {
        'lda': build_lda_model,
        'lsi': build_lsi_model
    }

# def build_model(dictionary, corpus, config, should_rebuild, BACKUP_FILE):
def build_model(dictionary, corpus, should_rebuild):
    try:
        model_build_fn = model_switch_dict()[cfg.MODEL_NAME]

        return model_build_fn(dictionary, corpus, should_rebuild)
    except Exception as exc:
        print_exception_details('Building Model', exc)


def build_lda_model(dictionary, corpus, should_rebuild):
    lda = []

    # DEBUG
    # should_rebuild = True

    # debug_print('datapath:LDA', datapath(cfg.LDA_BACKUP))

    if not should_rebuild:
        try:
            print('Loading LDA Model backup...')
            lda_file = get_file_path(cfg.LDA_BACKUP)
            print('LDA file = {}'.format(lda_file))

            # with open(LDA, "a") as lda_file:
                # if lda_file:
            lda = models.LdaModel.load(lda_file)

        except Exception as exc:
           print_exception_details('Building LDA Model', exc)

    else:
        print('Building LDA Model...')
        lda = models.LdaModel(corpus, id2word=dictionary, random_state=cfg.RANDOM_STATE, num_topics=cfg.NUM_TOPICS, passes=cfg.NUM_PASSES)
        print('Done!')
        # Save Model Structures
        LDA_FILE = get_file_path(cfg.LDA_BACKUP)
        lda.save(LDA_FILE)

    return lda

def build_lsi_model(dictionary, corpus, config, should_rebuild, LSI_BACKUP):
    lsi = []
    if not should_rebuild:
        try:
            LSI = get_file_path(LSI_BACKUP)
            print('LSI_FILE = {}'.format(LSI))

            if os.stat(LSI).st_size != 0:
                # print('LDA_FILE = {}'.format(LDA))
                with open(LSI, "a") as lsi_file:
                    if lsi_file:
                        print('Loading LSI File.')
                        lsi = models.LsiModel.load(lsi_file)
            else:
                print('Building LSI Model...')
                lsi = models.LdaModel(corpus, id2word=dictionary, random_state=config['RANDOM_STATE'], num_topics=config['NUM_TOPICS'], passes=config['PASSES'])
                print('Done!')
                # Save Model Structures
                LSI_FILE = get_file_path(LSI_BACKUP)
                lsi.save(LSI_FILE)
        except:
            print(' *** Error Loadind LSI Model!')
            print('Building LSI Model...')
            lsi = models.LdaModel(corpus, id2word=dictionary, random_state=config['RANDOM_STATE'], num_topics=config['NUM_TOPICS'], passes=config['PASSES'])
            print('Done!')
            # Save Model Structures
            LSI_FILE = get_file_path(LSI_BACKUP)
            lsi.save(LSI_FILE)

    else:
        print('Building LSI Model...')
        lsi = models.LsiModel(corpus, id2word=dictionary, random_state=config['RANDOM_STATE'], num_topics=config['NUM_TOPICS'], passes=config['PASSES'])
        print('Done!')
        # Save Model Structures
        LSI_FILE = get_file_path(LSI_BACKUP)
        lsi.save(LSI_FILE)

    return lsi

def get_unique_matrix_sim_values(sims, content, page_ids):
    pids = []
    index = 0
    result = 10

    # REFINEMENT: Possible to get "top 3-5" recommendations for pages
    #   based on "confidence" of passed in topic_details?


    while result > 0:
        page_ids_index = sims[index][0]
        page_id = page_ids[page_ids_index][0]
     
        if [page_id] not in pids:
            pids.append(page_id)
            # print('Page ID: {}'.format(page_id))
            # print('URL: {}'.format(content.get_page_url_by_id(page_id)))
            result -= 1
        index += 1
    
    return pids

    