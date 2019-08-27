from flask import request, send_from_directory, send_file, escape
from flask_restful import Resource, Api

import utils

# ### Data Stores and backups
DATABASE_FILE = './data/wiki_content.db'
LDA_BACKUP    = './data/lda_model'
LSI_BACKUP    = './data/lsi_model'
DICT_BACKUP   = './data/dictionary'
CORPUS_BACKUP = './data/corpus'

class LdaModelingServer(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        result = {}
        if 'query' in json_data:
            FILES = {'DICT': DICT_BACKUP, 'CORPUS': CORPUS_BACKUP}
            # query_model(model_name, content, should_rebuild, FILES, query)
            result.update( utils.query_model('lda', xxx, yyy, FILES, json_data['query']) )
        else:
            result = 'Error: INVALID JSON REQUEST'
        
        return result

class LsiModelingServer(Resource):
    def post(self, model_name):
        json_data = request.get_json(force=True)
        result = {}
        if 'query' in json_data:
            result.update( utils.query_model('lsi', json_data['query']) )
        else:
            result = 'Error: INVALID JSON REQUEST'
        
        return result