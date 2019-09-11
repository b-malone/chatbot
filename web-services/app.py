"""
    LDA\LSI Topic Modeling Service
        Listen for HTTP requests and return a JSON list of (related topic) documents.
"""
import logging
import pickle
import argparse
from optparse import OptionParser
from gensim import utils
from flask import Flask, request, send_from_directory, send_file, jsonify, escape
from flask_restful import Resource, Api
# from flask import g # "ENV vars" for flask apps
from werkzeug.exceptions import HTTPException, default_exceptions
from colored_logging import ColoredLogger
# import content
import utils
from topics_service import LdaModelingServer, LsiModelingServer


# ### Enable logging for Gensim
# logging.basicConfig(format='%(asctime)s : %(levelnam)s : %(message)s', level=logging.INFO)
logging.setLoggerClass(ColoredLogger)

# ARGS
# ### --rebuild (force rebuild of model)
parser = OptionParser()
parser.add_option('-m', '--model', nargs='?', type=str, default='lda', help='Select the Model to use for Topic Modeling (LDA, LSI, NMF)')
parser.add_option('-r', '--rebuild', nargs='?', default=False, help='Force rebuild of model')

(options, args) = parser.parse_args()
# parser = argparse.ArgumentParser(description='')
# parser.add_argument('--model', nargs='?', type=str, default='lda', help='Select the Model to use for Topic Modeling (LDA, LSI, NMF)')
# parser.add_argument('--rebuild', nargs='?', type=bool, default=False, help='Force rebuild of model')
# args, unknown = parser.parse_args()
### ARGS PARSING
if options.rebuild is None:
    options.rebuild = False 
else:
    options.rebuild = False 

should_rebuild = options.rebuild
MODEL_NAME = options.model
print('MODEL_NAME: {}'.format(MODEL_NAME))
print( type(MODEL_NAME) )
print('SHOULD_REBUILD: {}'.format(should_rebuild))
print( type(should_rebuild) )

# g.should_rebuild = should_rebuild
# g.MODEL_NAME = MODEL_NAME

# Serve && Run (Queries)!
PORT = 5000
app = Flask(__name__,static_url_path='')
api = Api(app)

#
# python -m flask run
#   FLASK_APP=main.py FLASK_DEBUG=1 python -m flask run
#   FLASK_DEBUG=1 => livereload
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

# Disable Caching (Development)
app.config["CACHE_TYPE"] = "null"
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Watch files and restart on changes

# DEBUG
@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

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


