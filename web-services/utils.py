import os
import string
import pickle
import json
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import similarities, corpora, models

lemma = WordNetLemmatizer()
punctuation = set(string.punctuation)
stoplist = set(stopwords.words('english'))


def variable_is_defined(var):
    return 'var' in vars() or 'var' in globals()

def get_similarity(lda, corpus, q_vec):
    """
    Find related Documents.
    """
    index = similarities.MatrixSimilarity(lda[corpus])
    sims = index[q_vec]
    return sims

def get_file_path(rel_filepath):
    # dir_path = os.path.split( os.path.dirname(__file__) )
    # print('dir_path = {}'.format(dir_path))
    # path = os.path.join(dir_path[0], rel_filepath)
    # print('path = {}'.format(path))
    script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
    script_dir  = os.path.split(script_path)[0] #i.e. /path/to/dir/
    # rel_path = "2091/data.txt"
    abs_file_path = os.path.join(script_dir, rel_filepath)

    return abs_file_path

def remove_punctuation(text):
    return ''.join(char for char in text if char not in punctuation)

def remove_numbers(text):
    return ''.join(char for char in text if not char.isdigit())

def remove_stop_words(text):
    return ' '.join([word for word in text.split() if word not in stoplist])

def remove_single_characters(text):
    return ' '.join([word for word in text.split() if len(word) > 1])

def lemmatize(text):
    return ' '.join([lemma.lemmatize(word) for word in text.split()])

def pickle_save(PATH, data):
    with open(PATH, "wb") as fp:
        pickle.dump(data, fp)
    fp.close()

# def serialize_json(PATH, data):
#     with open(PATH+'.json', 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

# def load_json_file(PATH):
#     json_data = {}
#     with open(PATH+'.json', 'r') as f:
#         json_data = json.load(f)
#     return json_data

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
    """
    dictionary = []
    DICT_FILE = get_file_path(DICT_BACKUP)

    if not should_rebuild:
        try:
            with open(DICT, "rb") as dict_file:
                if dict_file:
                    print('Loading Dictionary File.')
                    # load dict from disk
                    dictionary = corpora.dictionary.load(dict_file)
                    print('Dictionary Size = {}'.format(len(dictionary)))
        except:
            print('ERROR Building Dictionary!')
    else:
        print('Building Dictionary...')
        dictionary = corpora.Dictionary(content)    # list: (word_id, appearance count)
        dictionary.filter_extremes(no_below=5, no_above=0.4)
        # SAVE the construction
        dictionary.save(DICT_FILE)  # save dict to disk
        print('Dictionary Size = {}'.format(len(dictionary)))
    
    return dictionary

def build_corpus(dictionary, content, should_rebuild, CORPUS_BACKUP):
    """
        A (Gensim) Corpus is a "bag of words", which is a histogram map
        for unique and relevant words in a document.
    """
    corpus = []
    CORPUS_FILE = get_file_path(CORPUS_BACKUP)

    if not should_rebuild:
        try:
            with open(CORPUS_FILE, "rb") as corp_file:
                if corp_file:
                    print('Loading Corpus File.')
                    # corpus = pickle.load(corp_file)
                    corpus = corpora.MmCorpus(corp_file+'.mm')
                    print('Corpus Size = {}'.format(len(corpus)))
        except:
            print('ERROR Building Corpus!')
    else:
        print('Building Corpus...')
        corpus = [dictionary.doc2bow(text) for text in content] # doc-to-bag_of_words
        # SAVE the construction
        # corpus.save(CORPUS_FILE)  # save corpus to disk
        corpora.MmCorpus.serialize(CORPUS_FILE+'.mm', corpus) # save corpus to disk
        print('Corpus Size = {}'.format(len(corpus)))

    return corpus

def model_switch_dict():
    return {
        'lda': build_lda_model,
        'lsi': build_lsi_model
    }

def build_model(dictionary, corpus, config, should_rebuild, BACKUP_FILE):
    # try:
    model_build_fn = model_switch_dict()[config['MODEL_NAME']]

    return model_build_fn(dictionary, corpus, config, should_rebuild, BACKUP_FILE)
    # except:
    #     print('Unrecognized Model Name!')
    #     return {}


def build_lda_model(dictionary, corpus, config, should_rebuild, LDA_BACKUP):
    lda = []
    if not should_rebuild:
        try:
            LDA = get_file_path(LDA_BACKUP)
            if os.stat(LDA).st_size != 0:
                # print('LDA_FILE = {}'.format(LDA))
                with open(LDA, "a") as lda_file:
                    if lda_file:
                        print('Loading LDA File.')
                        lda = models.LdaModel.load(lda_file)
            else:
                print('Building LDA Model...')
                lda = models.LdaModel(corpus, id2word=dictionary, random_state=config['RANDOM_STATE'], num_topics=config['NUM_TOPICS'], passes=config['PASSES'])
                print('Done!')
                # Save Model Structures
                LDA_FILE = get_file_path(LDA_BACKUP)
                lda.save(LDA_FILE)
        except:
            print(' *** Error Loadind LDA Model!')
            print('Building LDA Model...')
            lda = models.LdaModel(corpus, id2word=dictionary, random_state=config['RANDOM_STATE'], num_topics=config['NUM_TOPICS'], passes=config['PASSES'])
            print('Done!')
            # Save Model Structures
            LDA_FILE = get_file_path(LDA_BACKUP)
            lda.save(LDA_FILE)

    else:
        print('Building LDA Model...')
        lda = models.LdaModel(corpus, id2word=dictionary, random_state=config['RANDOM_STATE'], num_topics=config['NUM_TOPICS'], passes=config['PASSES'])
        print('Done!')
        # Save Model Structures
        LDA_FILE = get_file_path(LDA_BACKUP)
        lda.save(LDA_FILE)

    return lda

def build_lsi_model(dictionary, corpus, config, should_rebuild, LSI_BACKUP):
    lsi = []
    if not should_rebuild:
        try:
            LSI = get_file_path(LSI_BACKUP)
            with open(LSI, "a") as lsi_file:
                if lsi_file:
                    print('Loading LSI File.')
                    lsi = models.LsiModel.load(lsi_file)

        except:
            print('Error Loadind LSI Model! Rebuilding...')
            print('Building LSI Model...')
            lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=config['NUM_TOPICS'])
            print('Done!')
            # Save Model Structures
            lsi.save(LSI_BACKUP)

    else:
        print('Building LSI Model...')
        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=config['NUM_TOPICS'])
        print('Done!')
        # Save Model Structures
        lsi.save(LSI_BACKUP)

    return lsi

def get_unique_matrix_sim_values(sims, content, page_ids):
    pids = []
    index = 0
    result = 10

    while result > 0:
        page_id = page_ids[sims[index][0]]
        if page_id not in pids:
            pids.append(page_id)
            print('Page ID: {}'.format(page_id))
            print('URL: {}'.format(content.get_page_url_by_id(page_id)))
            result -= 1
        index += 1
    
    return pids

    