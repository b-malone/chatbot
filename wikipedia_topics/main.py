#!/usr/bin/env python3
# Imports and Config
# #########################
import os
import pickle
import json
import sqlite3
import string
import logging 
# import pickle 

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
NUM_TOPICS=75
RANDOM_STATE=1
# ### LOGGING for Gensim
logging.basicConfig()
# ### Data Stores and backups
DATABASE_FILE = 'data/wiki_content.db'
LDA_BACKUP = 'data/lda_model'
DICT_BACKUP = 'data/dictionary'
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
dictionary = utils.build_dictionary(content, DICT_BACKUP)

# Create a Corpus
corpus = utils.build_corpus(dictionary, content, CORPUS_BACKUP)

# Build LDA Model
model_config = {}
model_config['RANDOM_STATE'] = RANDOM_STATE
model_config['NUM_TOPICS'] = NUM_TOPICS
model_config['PASSES'] = NUM_PASSES
lda = utils.build_lda_model(dictionary, corpus, model_config, LDA_BACKUP)

print('Counting Topics...')
topics = lda.print_topics(10) # Topic ~ set of (related) words
print(topics)

# ??? Topics Count
# print('Counting Topics...')
lda.print_topics(10) # Topic ~ set of (related) words



# # Save Model Structures
# lda.save(LDA_BACKUP)
# with open(DICT_BACKUP, "wb") as fp:
#     pickle.dump(dictionary, fp)
# fp.close()
# with open(CORPUS_BACKUP, "wb") as fp:
#     pickle.dump(corpus, fp)
# fp.close()
# with open(LDA_BACKUP, "wb") as fp:
#     pickle.dump(lda, fp)
# fp.close()

# Run Queries!
# #########################

# query_1 = "using deep learning for computer vision in real time"
# # FIND Statistically important words according to our parameters...
# bow = dictionary.doc2bow(utils.get_cleaned_text(query).split())
# bag_of_words = [word for word in bow]

# for word in bag_of_words:
#     print('{}: {}'.format(word[0], dictionary[word[0]]))
# # deep, learning, real, time, using, vision ...

# # Run Model on bag_of_words
# q_vec = lda[bow]    # "query vector"
# # print(q_vec)
# # ### LDA Topic Result Details
# topic_details = lda.print_topic(max(q_vec, key=lambda item: item[1])[0])
# # print(topic_details)

# # ### Get Similarity of Query Vector to Document Vectors
# sims = get_similarity(lda, q_vec)
# # Sort High-to-Low by similarity
# sims = sorted(enumerate(sims), key=lambda item: -item[1])

# pids = utils.get_unique_matrix_sim_values(sims, page_ids)