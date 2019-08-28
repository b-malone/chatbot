import os
# import json
from flask import send_from_directory, send_file, escape, jsonify
from flask_restful import Resource, Api, request
from gensim import corpora

import content
import utils

# ### Data Stores and backups
DATABASE_FILE = 'data/wiki_content.db'
LDA_BACKUP    = 'data/lda_model'
LSI_BACKUP    = 'data/lsi_model'
DICT_BACKUP   = 'data/dictionary'
CORPUS_BACKUP = 'data/corpus'

# Model Configuration 
NUM_PASSES=10
NUM_TOPICS=100
RANDOM_STATE=1
MODEL_NAME='lda'

# Configuration for modeling
model_config = {}
model_config['RANDOM_STATE'] = RANDOM_STATE if utils.variable_is_defined(RANDOM_STATE) else 1
model_config['NUM_TOPICS'] = NUM_TOPICS if utils.variable_is_defined(NUM_TOPICS) else 100
model_config['PASSES'] = NUM_PASSES if utils.variable_is_defined(NUM_PASSES) else 10
model_config['MODEL_NAME'] = MODEL_NAME if utils.variable_is_defined(MODEL_NAME) else 'lda'


def load_content():
    # Access DataBase content, 
    # build content (Object) for modeling and analysis
    DATABASE = utils.get_file_path(DATABASE_FILE)
    return content.Content(DATABASE)

def build_dictionary(content):
    # Create a Dictionary
    ## Vector Space of words and word_count
    if os.path.exists(DICT_BACKUP+'.json'):
        should_rebuild = os.stat(DICT_BACKUP+'.json').st_size == 0
    else:
        should_rebuild = True

    return utils.build_dictionary(content, should_rebuild, DICT_BACKUP)

def build_corpus(dictionary, content):
    # Create a Corpus
    if os.path.exists(CORPUS_BACKUP+'.json'):
        should_rebuild = os.stat(CORPUS_BACKUP+'.json').st_size == 0
    else:
        should_rebuild = True

    return utils.build_corpus(dictionary, content, should_rebuild, CORPUS_BACKUP)
    # print('Corpus Size: {}'.format( len(corpus) ))

def build_predictive_model(dictionary, corpus):
    # Build Model!
    BACKUP_FILE = 'data/' + model_config['MODEL_NAME'].lower() + '_model'
    should_rebuild = os.stat(BACKUP_FILE).st_size == 0
    # print('building model {}...'.foramat(model_config['MODEL_NAME']))
    return utils.build_model(dictionary, corpus, model_config, should_rebuild, BACKUP_FILE)

def switch_model_backup_file(model_name):
    switcher = {'lda': LDA_BACKUP, 'lsi': LSI_BACKUP}
    return switcher.get(model_name)

def query_model(model_name, content, should_rebuild, FILES, query):
    # Create a Dictionary
    ## Vector Space of words and word_count
    dictionary = build_dictionary(content)

    # Create a Corpus
    corpus = build_corpus(dictionary, content)

    # bow = corpora.Dictionary().doc2bow(utils.get_cleaned_text( query ).split())
    bow = dictionary.doc2bow(utils.get_cleaned_text( query ).split())
    # bag_of_words = [word for word in bow]

    
    # ###########################
    # <class 'list'>
    # ###########################
    # [(1506, 1), (2189, 1), (2746, 1), (3192, 1), (3316, 1)]
    # ###########################
    ###########################
    # <class 'list'>
    # ###########################
    # [(1506, 1), (2189, 1), (2746, 1), (2761, 1), (3192, 1), (3681, 1)]
    # ###########################
    model = build_predictive_model(dictionary, corpus)


    # ###########################
    # <class 'gensim.models.ldamodel.LdaModel'>
    # ###########################
    # LdaModel(num_terms=26033, num_topics=100, decay=0.5, chunksize=2000)
    # ###########################
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #  *** Error Loadind LDA Model!
    # ###########################
    # <class 'list'>
    # ###########################
    # []
    # ###########################
    print('###########################')
    print( type(model) )
    print('###########################')
    print( model )
    print('###########################')

    # MODEL
    # BACKUP_FILE = switch_model_backup_file(model_name)
    # model = build_predictive_model(dictionary, corpus)
    q_vec = model[bow]    # "query vector"
    topic_details = model.print_topic(max(q_vec, key=lambda item: item[1])[0])

    # ### Get Similarity of Query Vector to Document Vectors
    sims = utils.get_similarity(model, corpus, q_vec)
    # Sort High-to-Low by similarity
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    # ###
    # RECCOMMEND/TOPICS RESULT:
    # ### Get Related Pages
    pids = utils.get_unique_matrix_sim_values(sims, content, content.get_page_ids())
    return pids 

    # result = {}
    # for pid in pids:
    #     result[pid] = content.get_page_url_by_id(pid)
    
    # return result

    # # "Swtich Map" model functions
    # def lda():  
    # return []


# def lda_model_response(query):
#     # json_data = request.get_json(force=True)
#     result = {}
#     if query: # 'query' in json_data:
#         FILES = {'DICT': DICT_BACKUP, 'CORPUS': CORPUS_BACKUP}
#         should_rebuild = os.stat(LDA_BACKUP).st_size == 0
#         content = load_content()
#         # Query the Model
#         # query_model(model_name, content, should_rebuild, FILES, query)
#         # result.update( query_model('lda', content, should_rebuild, FILES, json_data['query']) )
#         result.update( query_model('lda', content, should_rebuild, FILES, query) )
#     else:
#         result = 'Error: INVALID JSON REQUEST'
    
#     return result

class LdaModelingServer(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        result = {}
        if 'query' in json_data:
            FILES = {'DICT': DICT_BACKUP, 'CORPUS': CORPUS_BACKUP}
            should_rebuild = os.stat(LDA_BACKUP).st_size == 0
            content = load_content()
            
            # Query the Model
            result = jsonify( query_model('lda', content, should_rebuild, FILES, json_data['query']) )
        else:
            result = 'Error: INVALID JSON REQUEST'
        
        return result

class LsiModelingServer(Resource):
    def post(self, model_name):
        json_data = request.get_json(force=True)
        result = {}
        if 'query' in json_data:
            FILES = {'DICT': DICT_BACKUP, 'CORPUS': CORPUS_BACKUP}
            should_rebuild = os.stat(LSI_BACKUP).st_size == 0
            content = load_content()
            # Query the Model
            result.update( query_model('lsi', content, should_rebuild, FILES, json_data['query']) )
        else:
            result = 'Error: INVALID JSON REQUEST'
        
        return result