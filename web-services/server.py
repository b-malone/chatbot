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
    # BUG: Saved Dictionaries are not of Type Dictionary!
    # should_rebuild = not utils.try_to_open_file(DICT_BACKUP)
    should_rebuild = True
    # print('Should Rebuild Dictionary = {}'.format(should_rebuild))

    return utils.build_dictionary(content, should_rebuild, DICT_BACKUP)

def build_corpus(dictionary, content):
    # Create a Corpus
    # BUG: Saved Corpuses are not of Type Corpus!
    # should_rebuild = not utils.try_to_open_file(CORPUS_BACKUP)
    should_rebuild = True
    # print('Should Rebuild Corpus = {}'.format(should_rebuild))
    return utils.build_corpus(dictionary, content, should_rebuild, CORPUS_BACKUP)
    # print('Corpus Size: {}'.format( len(corpus) ))

def build_predictive_model(model_name, dictionary, corpus):
    # Build Model!
    BACKUP_FILE = 'data/' + model_name.lower() + '_model'
    # BUG: Saved Models are not of Type Model!
    should_rebuild = not utils.try_to_open_file(BACKUP_FILE)

    print('###########################')
    print('Model_Name = {}'.format(model_name))
    print('###########################')

    print('Should Rebuild Model = {}'.format(should_rebuild))

    # print('building model {}...'.foramat(model_config['MODEL_NAME']))
    model_config['MODEL_NAME'] = model_name
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

    model = build_predictive_model(model_name, dictionary, corpus)

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
    # return pids 

    print('###########################')
    print( topic_details )
    print('###########################')

    result = {}
    for pid in pids:
        url = content.get_page_url_by_id(pid)
        # print('###########################')
        # print( pid )
        # print( url[0] if isinstance(url, tuple) else url )
        # print('###########################')
        result[pid] = url[0] if isinstance(url, tuple) else url
    
    # print('###########################')
    # print( result )
    # print('###########################')
    return result

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
        model_config['MODEL_NAME'] = 'lda'
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
    def post(self):
        model_config['MODEL_NAME'] = 'lsi'
        json_data = request.get_json(force=True)
        result = {}
        if 'query' in json_data:
            FILES = {'DICT': DICT_BACKUP, 'CORPUS': CORPUS_BACKUP}
            should_rebuild = os.stat(LSI_BACKUP).st_size == 0
            content = load_content()

            # Query the Model
            result = jsonify( query_model('lsi', content, should_rebuild, FILES, json_data['query']) )
        else:
            result = 'Error: INVALID JSON REQUEST'
        
        return result