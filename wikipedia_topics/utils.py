import os
import string
import pickle
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import similarities, corpora, models

lemma = WordNetLemmatizer()
punctuation = set(string.punctuation)
stoplist = set(stopwords.words('english'))


def get_similarity(lda, corpus, q_vec):
    """
    Find related Documents.
    """
    index = similarities.MatrixSimilarity(lda[corpus])
    sims = index[q_vec]
    return sims

def get_file_path(rel_filepath):
    dir_path = os.path.split( os.path.dirname(__file__) )
    # print('dir_path = {}'.format(dir_path))
    path = os.path.join(dir_path[0], rel_filepath)
    # print('path = {}'.format(path))
    return path

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
    dictionary = []

    if not should_rebuild:
        try:
            DICT = get_file_path(DICT_BACKUP)
            with open(DICT, "rb") as dict_file:
                if dict_file:
                    print('Loading Dictionary File.')
                    dictionary = pickle.load(dict_file)
                    print('Dictionary Size = {}'.format(len(dictionary)))
        except:
            print('ERROR Building Dictionary!')
    else:
        print('Building Dictionary...')
        dictionary = corpora.Dictionary(content)    # list: (word_id, appearance count)
        dictionary.filter_extremes(no_below=5, no_above=0.4)
        # SAVE the construction
        pickle_save(DICT_BACKUP, dictionary)
        print('Dictionary Size = {}'.format(len(dictionary)))

    # except:
    #     print('Building Dictionary...')
    #     dictionary = corpora.Dictionary(content)    # list: (word_id, appearance count)
    #     dictionary.filter_extremes(no_below=5, no_above=0.4)
    #     # SAVE the construction
    #     self.pickle_save(DICT_BACKUP, dictionary)
    #     print('Dictionary Size = {}'.format(len(dictionary)))
    
    return dictionary

def build_corpus(dictionary, content, should_rebuild, CORPUS_BACKUP):
    corpus = []
    if not should_rebuild:
        try:
            CORPUS = get_file_path(CORPUS_BACKUP)
            with open(CORPUS, "rb") as corp_file:
                if corp_file:
                    print('Loading Corpus File.')
                    corpus = pickle.load(corp_file)
                    print('Corpus Size = {}'.format(len(corpus)))
        except:
            print('ERROR Building Corpus!')
    else:
        print('Building Corpus...')
        corpus = [dictionary.doc2bow(text) for text in content] # doc-to-bag_of_words
        # SAVE the construction
        pickle_save(CORPUS_BACKUP, corpus)
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
            print('LDA_FILE = {}'.format(LDA))
            with open(LDA, "a") as lda_file:
                if lda_file:
                    print('Loading LDA File.')
                    lda = models.LdaModel.load(lda_file)
        except:
            print('ERROR Building LDA Model!')

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
            print('ERROR Building LSI Model!')

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
            print('Page ID {}: {}'.format(page_id[0]), content.get_page_url_by_id(page_id[0]))
            result -= 1
        index += 1
    
    return pids

    