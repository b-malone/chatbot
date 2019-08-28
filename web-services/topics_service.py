"""
    LDA\LSI Topic Modeling Service
        Listen for HTTP requests and return a JSON list of (related topic) documents.
"""
import logging
import pickle
import argparse
from gensim import utils
from flask import Flask, request, send_from_directory, send_file, jsonify
from flask_restful import Resource, Api
from werkzeug.exceptions import HTTPException, default_exceptions

# import content
import utils
from server import LdaModelingServer, LsiModelingServer


# ### Enable logging for Gensim
logging.basicConfig(format='%(asctime)s : %(levelnam)s : %(message)s', level=logging.INFO)
# # ### Data Stores and backups
# DATABASE_FILE = './data/wiki_content.db'
# LDA_BACKUP    = './data/lda_model'
# LSI_BACKUP    = './data/lsi_model'
# DICT_BACKUP   = './data/dictionary'
# CORPUS_BACKUP = './data/corpus'

# ARGS
# ### --rebuild (force rebuild of model)
parser = argparse.ArgumentParser(description='')
parser.add_argument('--model', nargs='?', type=str, default='lda', help='Select the Model to use for Topic Modeling (LDA, LSI, NMF)')
parser.add_argument('--rebuild', nargs='?', type=bool, default=False, help='Force rebuild of model')
args = parser.parse_args()
### ARGS PARSING
if args.rebuild is None:
    args.rebuild = True

should_rebuild = args.rebuild
MODEL_NAME = args.model
print('MODEL_NAME: {}'.format(MODEL_NAME))
print( type(MODEL_NAME) )
print('SHOULD_REBUILD: {}'.format(should_rebuild))
print( type(should_rebuild) )

# RUN!
# Model, stores
# dictionary = corpora.Dictionary()
# lemma = WordNetLemmatizer()

# # Access DataBase content, 
# # build content (Object) for modeling and analysis
# DATABASE = utils.get_file_path(DATABASE_FILE)
# content = content.Content(DATABASE)

# # Create a Dictionary
# ## Vector Space of words and word_count
# dictionary = utils.build_dictionary(content, should_rebuild, DICT_BACKUP)

# # Create a Corpus
# corpus = utils.build_corpus(dictionary, content, should_rebuild, CORPUS_BACKUP)
# print('Corpus Size: {}'.format( len(corpus) ))

# # Configuration for modeling
# model_config = {}
# model_config['RANDOM_STATE'] = RANDOM_STATE if utils.variable_is_defined(RANDOM_STATE) else 1
# model_config['NUM_TOPICS'] = NUM_TOPICS if utils.variable_is_defined(NUM_TOPICS) else 100
# model_config['PASSES'] = NUM_PASSES if utils.variable_is_defined(NUM_PASSES) else 10
# model_config['MODEL_NAME'] = MODEL_NAME if utils.variable_is_defined(MODEL_NAME) else 'lda'

# # Build Model!
# BACKUP_FILE = 'data/' + model_config['MODEL_NAME'].lower() + '_model'
# print('building model {}...'.foramat(model_config['MODEL_NAME']))
# model = utils.build_model(dictionary, corpus, model_config, should_rebuild, BACKUP_FILE)


# Serve && Run (Queries)!
PORT = 5000
app = Flask(__name__,static_url_path='')
api = Api(app)

#
# curl --header "Content Type: application/json" --request POST --data '{"query" :""}' URL
#

# @app.route("/topics/lda", methods=['POST'])
# def lda():
#     if request.method == 'POST':
#         # note = str(request.data.get('text', ''))
#         query = request.data.get('query', '')
#         return lda_model_response(query)

# api.add_resource(TopicModelingServer, '/topics')
api.add_resource(LdaModelingServer, '/topics/lda')
api.add_resource(LsiModelingServer, '/topics/lsi')

# Handle/Return Errors (Debugging)
def handle_error(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
    return jsonify(error='error', code=code)

for exc in default_exceptions:
    app.register_error_handler(exc, handle_error)

if __name__ == '__main__':
    # $ python lda_service.py => http://localhost:5000/lda
    app.run(host='0.0.0.0', port=PORT)

# @app.route('/')
# def hello():
#     name = request.args.get("name", "World")
#     return f'Hello, {escape(name)}!'
