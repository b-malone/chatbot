#!/usr/bin/env python

# File Storage Paths
DATABASE_FILE = 'data/help.db'
LDA_BACKUP    = 'data/lda_model.model'
LSI_BACKUP    = 'data/lsi_model.model'
DICT_BACKUP   = 'data/dictionary'
CORPUS_BACKUP = 'data/corpus.mm'

# Model Configuration 
NUM_PASSES=10
NUM_TOPICS=100
RANDOM_STATE=1
MODEL_NAME='lda'

# # Configuration for modeling
# model_config = {}
# model_config['RANDOM_STATE'] = RANDOM_STATE
# model_config['NUM_TOPICS'] = NUM_TOPICS
# model_config['PASSES'] = NUM_PASSES
# model_config['MODEL_NAME'] = MODEL_NAME
