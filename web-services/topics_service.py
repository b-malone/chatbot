import os
# import json
from flask import send_from_directory, send_file, escape, jsonify
from flask_restful import Resource, Api, request
from gensim import corpora

# import content
import help_content
# from help_content import HelpContent as content
import utils
import config as cfg



def load_content():
    # Access DataBase content, 
    # build content (Object) for modeling and analysis
    DATABASE = utils.get_file_path(cfg.DATABASE_FILE)
    content = help_content.HelpContent(DATABASE)
    
    # for text in content.get_cleaned_pages()[0:5]:
    #     utils.debug_print('text', text)

    return content # .get_cleaned_pages()


def build_dictionary(content):
    # Create a Dictionary
    # BUG: Saved Dictionaries are not of Type Dictionary!
    should_rebuild = not utils.try_to_open_file(cfg.DICT_BACKUP)
    # should_rebuild = True
    # print('Should Rebuild Dictionary = {}'.format(should_rebuild))

    return utils.build_dictionary(content.get_cleaned_pages(), should_rebuild, cfg.DICT_BACKUP)

def build_corpus(dictionary, content):
    # Create a Corpus
    # BUG: Saved Corpuses are not of Type Corpus!
    should_rebuild = not utils.try_to_open_file(cfg.CORPUS_BACKUP)
    # should_rebuild = True
    # print('Should Rebuild Corpus = {}'.format(should_rebuild))
    return utils.build_corpus(dictionary, content.get_cleaned_pages(), should_rebuild, cfg.CORPUS_BACKUP)
    # print('Corpus Size: {}'.format( len(corpus) ))

def build_predictive_model(model_name, dictionary, corpus):
    # Build Model!
    BACKUP_FILE = 'data/' + model_name.lower() + '_model.model'
    # BUG: Saved Models are not of Type Model!
    should_rebuild = not utils.try_to_open_file(BACKUP_FILE)

    # print('###########################')
    # print('Model_Name = {}'.format(model_name))
    # print('###########################')

    print('Should Rebuild Model = {}'.format(should_rebuild))

    # print('building model {}...'.foramat(model_config['MODEL_NAME']))
    cfg.MODEL_NAME = model_name
    return utils.build_model(dictionary, corpus, should_rebuild)

def switch_model_backup_file(model_name):
    switcher = {'lda': cfg.LDA_BACKUP, 'lsi': cfg.LSI_BACKUP}
    return switcher.get(model_name)

def query_model(model_name, content, should_rebuild, FILES, query):
    # Create a Dictionary
    ## Vector Space of words and word_count
    dictionary = build_dictionary(content)

    # Create a Corpus
    corpus = build_corpus(dictionary, content)

    # bow = corpora.Dictionary().doc2bow(utils.get_cleaned_text( query ).split())
    bow = dictionary.doc2bow(utils.get_cleaned_text( query.lower() ).split())
    # bag_of_words = [word for word in bow]

    model = build_predictive_model(model_name, dictionary, corpus)

    # MODEL
    # BACKUP_FILE = switch_model_backup_file(model_name)
    # model = build_predictive_model(dictionary, corpus)
    q_vec = model[bow]    # "query vector"

    # Topic ID for "Max Coherence/Confidence Value"
    print('###########################')
    print("Q_Vec")
    print( q_vec )
    print('###########################')


    # ISSUES
    #
    #   * ValueError: max() arg is an empty sequence
    #   ??? Does this mean topic model matching FAILED ?
    #
    result = "NO VALID TOPICS! You want conversation??!"
    if len(q_vec) > 0 and cfg.MODEL_NAME in ['lda', 'lsi']:
        """
        Query => Help Topic, respond with recommendations
        """

        print( max(q_vec, key=lambda item: item[1]) )
        print('###########################')

        topic_details = model.print_topic( max(q_vec, key=lambda item: item[1])[0] )

        # ### Get Similarity of Query Vector to Document Vectors
        # "sims" ~ histpgram of topics? (1.0 ~ PRESENT, 0.0 ~ NOT PRESENT ?)
        sims = utils.get_similarity(model, corpus, q_vec)
        # Sort High-to-Low by similarity
        sims = sorted(enumerate(sims), key=lambda item: -item[1])

        # ###
        # RECCOMMEND/TOPICS RESULT:
        # ### Get Related Pages
        pids = utils.get_unique_matrix_sim_values(sims, content, content.get_page_ids())


        print('###########################')
        print( topic_details )
        print('###########################')

        result = {}
        for pid in pids:
            print( 'pid={}'.format(pid) )
            url = content.get_page_url_by_id(pid)
            result[pid] = url[0] if isinstance(url, tuple) else url
        
        # return result
    elif (len(q_vec) > 0 and cfg.MODEL_NAME == 'tfid'):


        print('###########################')
        print( model.__getitem__ )
        print('###########################')

        result = model.__getitem__

        # return result

    else:   
        """
        Query => NON-Help Topic, respond with conversation
        """
        # result = {}
        result = "NO VALID TOPICS! You want conversation??!"

        # return result

    return result


#
# To Do:
#   Enable passing POST data {'model': MODEL_NAME} to change model used
#
def parse_client_query(json_data, model_name, stored_model_file):
    if 'query' in json_data:
        FILES = {'DICT': cfg.DICT_BACKUP, 'CORPUS': cfg.CORPUS_BACKUP}
        # should_rebuild = os.stat(LDA_BACKUP).st_size == 0
        should_rebuild = not utils.try_to_open_file(stored_model_file)
        content = load_content()
        
        # Query the Model
        return jsonify( query_model(model_name, content, should_rebuild, FILES, json_data['query']) )
        # result = jsonify( query_model('lda', content, should_rebuild, FILES, json_data['query']) )
    else:
        return 'Error: INVALID JSON REQUEST'

class LdaModelingServer(Resource):
    def post(self):
        cfg.MODEL_NAME = 'lda'
        json_data = request.get_json(force=True)
        stored_model_file = cfg.LDA_BACKUP

        return parse_client_query(json_data, 'lda', stored_model_file)

class LsiModelingServer(Resource):
    def post(self):
        cfg.MODEL_NAME = 'lsi'
        json_data = request.get_json(force=True)
        stored_model_file = cfg.LDA_BACKUP

        return parse_client_query(json_data, 'lsi', stored_model_file)

class TfidModelingServer(Resource):
    def post(self):
        cfg.MODEL_NAME = 'tfid'
        json_data = request.get_json(force=True)
        stored_model_file = cfg.TFID_BACKUP
    
        return parse_client_query(json_data, 'tfid', stored_model_file)