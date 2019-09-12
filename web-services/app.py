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
from topics_service import LdaModelingServer, LsiModelingServer, TfidModelingServer


# ### Enable logging for Gensim
# logging.basicConfig(format='%(asctime)s : %(levelnam)s : %(message)s', level=logging.INFO)
logging.setLoggerClass(ColoredLogger)

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
# curl --header "Content-Type: application/json" --request POST --data '{"query": "how do I schedule an event?"}' http://localhost:5000/topics/lda
# curl --header "Content-Type: application/json" --request POST --data '{"query": "is this website accessible??"}' http://localhost:5000/topics/lda

# api.add_resource(TopicModelingServer, '/topics')
api.add_resource(LdaModelingServer, '/topics/lda')
api.add_resource(LsiModelingServer, '/topics/lsi')
api.add_resource(TfidModelingServer, '/topics/tfid')

# Disable Caching (Development)
app.config["CACHE_TYPE"] = "null"
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Watch files and restart on changes

# @app.route("/topics/lda", methods=['POST'])
# def lda():
#     if request.method == 'POST':
#         # note = str(request.data.get('text', ''))
#         query = request.data.get('query', '')
#         return lda_model_response(query)

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


