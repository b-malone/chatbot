#!/usr/bin/env python3
# Imports and Config
# #########################
import os
import sys
import pickle
import json
import sqlite3
import string
import logging 
import argparse

from gensim import utils, corpora # "fast" vector space modeling
from collections import defaultdict

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
# nltk.download('stopwords')
from nltk.corpus import wordnet
# nltk.download('wordnet')

import content
import utils

# Configuration 
NUM_PASSES=10
NUM_TOPICS=100
RANDOM_STATE=1
MODEL_NAME='lda'
# ### LOGGING for Gensim
logging.basicConfig()
# ### Data Stores and backups
DATABASE_FILE = 'data/wiki_content.db'
LDA_BACKUP    = 'data/lda_model'
LSI_BACKUP    = 'data/lsi_model'
DICT_BACKUP   = 'data/dictionary'
CORPUS_BACKUP = 'data/corpus'

# Setup and Model Building
# #########################
# from crawler.CrawlWikipedia import CrawlWikipedia

# CATEGORY='Category:Artificial_Intelligence'
# PAGE_LINK_DEPTH=1

# crawler = CrawlWikipedia(DATABASE)
# crawler.get_categories_and_members(CATEGORY, PAGE_LINK_DEPTH)

# punctuation = set(string.punctuation)
# stoplist = set(stopwords.words('english'))

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

# #########################

# LDA Model, stores
dictionary = corpora.Dictionary()
lemma = WordNetLemmatizer()

# Access DataBase content, 
# build content (Object) for modeling and analysis
# DATABASE=os.path.abspath(DATABASE_FILE)
DATABASE = utils.get_file_path(DATABASE_FILE)
content = content.Content(DATABASE)

# Create a Dictionary
## Vector Space of words and word_count
dictionary = utils.build_dictionary(content, should_rebuild, DICT_BACKUP)

# Create a Corpus
corpus = utils.build_corpus(dictionary, content, should_rebuild, CORPUS_BACKUP)
print('Corpus Size: {}'.format( len(corpus) ))

# Configuration for modeling
model_config = {}
model_config['RANDOM_STATE'] = RANDOM_STATE
model_config['NUM_TOPICS'] = NUM_TOPICS
model_config['PASSES'] = NUM_PASSES
model_config['MODEL_NAME'] = MODEL_NAME

# lda = utils.build_lda_model(dictionary, corpus, model_config, should_rebuild, LDA_BACKUP)
# # lsi = utils.build_lsi_model(dictionary, corpus, model_config, should_rebuild, LSI_BACKUP)

# Build Model!
BACKUP_FILE = 'data/' + MODEL_NAME.lower() + '_model'
model = utils.build_model(dictionary, corpus, model_config, should_rebuild, BACKUP_FILE)

if hasattr(model, 'print_topics'):
    print('Counting Topics...')
    topics = model.print_topics(10) # Topic ~ set of (related) words
    print(topics)

# ??? Topics Count
# print('Counting Topics...')
# lda.print_topics(10) # Topic ~ set of (related) words


# # Run Queries!
# # #########################

query_1 = "using deep learning for computer vision in real time"
# FIND Statistically important words according to our parameters...
bow = dictionary.doc2bow(utils.get_cleaned_text( query_1 ).split())
bag_of_words = [word for word in bow]

# DEBUG
# Bag Of Words ON Query
for word in bag_of_words:
    print('{}: {}'.format(word[0], dictionary[word[0]]))


# Run Model on bag_of_words
q_vec = model[bow]    # "query vector"
# print(q_vec)
print("==============")
# ### LDA Topic Result Details
topic_details = model.print_topic(max(q_vec, key=lambda item: item[1])[0])
print(topic_details)
print("==============")

# ### Get Similarity of Query Vector to Document Vectors
sims = utils.get_similarity(model, corpus, q_vec)
# Sort High-to-Low by similarity
sims = sorted(enumerate(sims), key=lambda item: -item[1])
# RECCOMMEND:
# ### Get Related Pages
pids = utils.get_unique_matrix_sim_values(sims, content, content.get_page_ids())

