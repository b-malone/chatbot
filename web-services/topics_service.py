import os
# import json
from flask import send_from_directory, send_file, escape, jsonify
from flask_restful import Resource, Api, request
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel

# import content
import help_content
# from help_content import HelpContent as content
import utils
import model_inputs
import config as cfg


def load_content():
    # Access DataBase content, 
    # build content (Object) for modeling and analysis
    DATABASE = utils.get_file_path(cfg.DATABASE_FILE)
    content = help_content.HelpContent(DATABASE)
    
    # for text in content.get_cleaned_pages()[0:5]:
    #     utils.debug_print('text', text)

    return content # .get_cleaned_pages()

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

def conversation_response():
    return "NO VALID TOPICS! You want conversation??!"

def switch_model_backup_file(model_name):
    switcher = {'lda': cfg.LDA_BACKUP, 'lsi': cfg.LSI_BACKUP}
    return switcher.get(model_name)

def query_model(model_name, content, bow, dictionary, FILES, query):
    """
    Given Help/Wiki Topic related query, index the model built on
    Help/Wiki content and provide reccomendations and information 
    for customer support/help.
    """
    result = {}
    # Create a Corpus
    # corpus = build_corpus(dictionary, content)
    corpus = model_inputs.build_corpus(dictionary, content.get_cleaned_pages(), cfg.CORPUS_BACKUP)
  
    model = build_predictive_model(model_name, dictionary, corpus)

    # MODEL
    q_vec = model[bow]    # "query vector"

    # DEBUG
    utils.debug_print('bow', bow)

    # Topic ID for "Max Coherence/Confidence Value" ??????
    # cm = CoherenceModel(model=model, corpus=corpus, topn=3, coherence='u_mass')    
    # coherence = cm.get_coherence()  # get coherence value
  
    # utils.debug_print('coherence', cm.top_topics_as_word_lists(model=model, dictionary=dictionary, topn=3))
    # utils.debug_print('coherence', cm.top_topics_as_word_lists)

    topic_details = model.print_topic( max(q_vec, key=lambda item: item[1])[0] )

    # ### Get Similarity of Query Vector to Document Vectors
    # "sims" ~ histpgram of topics? (1.0 ~ PRESENT, 0.0 ~ NOT PRESENT ?)
    sims = utils.get_similarity(model, corpus, q_vec)
    # Sort High-to-Low by similarity
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    # RECCOMMEND/TOPICS RESULT:
    # * Get Related Pages
    pids = utils.get_unique_matrix_similarity_values(sims, content, content.get_page_ids())

    # DEBUG
    utils.debug_print('topic_details', topic_details)

    result = {}
    for pid in pids:
        print( 'pid={}'.format(pid) )
        url = content.get_page_url_by_id(pid)
        result[pid] = url[0] if isinstance(url, tuple) else url

    return result


#
# To Do:
#   Enable passing POST data {'model': MODEL_NAME} to change model used
#
def parse_client_query(json_data, model_name, stored_model_file):
    """
    Parse and interpret the User's/Client's Query.
    Is it conversational, or a (relevant) Help or Wiki Topic seeking recommendations of help
    or information?
    """
    if 'query' in json_data:
        FILES = {'DICT': cfg.DICT_BACKUP, 'CORPUS': cfg.CORPUS_BACKUP}

        query = json_data['query']

        content = load_content()

        # IF necessary, (re)build Dictionary and Corpus on Content for Topic Modeling
        # Create a Dictionary
        # dictionary = build_dictionary(content)
        dictionary = model_inputs.build_dictionary(content.get_cleaned_pages(), cfg.DICT_BACKUP)

        # !!!!!!!!!!
        # CHAT QUERIES ST bow empty ([]) => Chat and NOT Topic Question???
        # !!!!!!!!!!
        ## Vector Space of words and word_count
        bow = dictionary.doc2bow(utils.get_cleaned_text( query.lower() ).split())
        # bag_of_words = [word for word in bow]
        
        # IS Query chatting or a Content/Help Topic Question?
        if len(bow) > 0:
            # Query the Model
            return jsonify( query_model(model_name, content, bow, dictionary, FILES, json_data['query']) )
            # result = jsonify( query_model('lda', content, should_rebuild, FILES, json_data['query']) )
        else:
            # Have a conversation with the User/Client
            return jsonify( conversation_response() )

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