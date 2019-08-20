#!/usr/bin/env python3
# Imports and Config
# #########################
import os
import json
import sqlite3
import string
import logging 
import pickle 

from gensim import corpora, utils, models # "fast" vector space modeling
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
DATABASE=utils.get_file_path(DATABASE_FILE)
content = content.Content(DATABASE)

# Create a Dictionary
## Vector Space of words and word_count
dictionary = []
try:
    DICT=utils.get_file_path(DICT_BACKUP)
    with open(DICT, "rb") as dict_file:
        if dict_file:
            print('Loading Dictionary File.')
            dictionary = pickle.load(dict_file)
            print('Dictionary Size = {}'.format(len(dictionary)))
        else:
            print('Building Dictionary...')
            dictionary = corpora.Dictionary(content)    # list: (word_id, appearance count)
            dictionary.filter_extremes(no_below=5, no_above=0.4)
            print('Dictionary Size = {}'.format(len(dictionary)))
except:
    print('Building Dictionary...')
    dictionary = corpora.Dictionary(content)    # list: (word_id, appearance count)
    dictionary.filter_extremes(no_below=5, no_above=0.4)
    print('Dictionary Size = {}'.format(len(dictionary)))

# Create a Corpus
corpus = []
try:
    CORPUS=utils.get_file_path(CORPUS_BACKUP)
    with open(CORPUS, "rb") as corp_file:
        if corp_file:
            print('Loading Corpus File.')
            corpus = pickle.load(corp_file)
            print('Corpus Size = {}'.format(len(corpus)))
        else:
            print('Building Corpus...')
            corpus = [dictionary.doc2bow(text) for text in content] # doc-to-bag_of_words
            print('Corpus Size = {}'.format(len(corpus)))
except:
    print('Building Corpus...')
    corpus = [dictionary.doc2bow(text) for text in content] # doc-to-bag_of_words
    print('Corpus Size = {}'.format(len(corpus)))

# Build LDA Model
lda = []
try:
    LDA=utils.get_file_path(LDA_BACKUP)
    with open(LDA, "rb") as lda_file:
        if lda_file:
            print('Loading LDA File.')
            lda = pickle.load(lda_file)
            print('Counting Topics...')
            lda.print_topics(10) # Topic ~ set of (related) words
        else:
            print('Building LDA Model...')
            lda = models.LdaModel(corpus, id2word=dictionary, random_state=RANDOM_STATE, num_topics=NUM_TOPICS, passes=NUM_PASSES)
            print('Done!')
            print('Counting Topics...')
            topics = lda.print_topics(10) # Topic ~ set of (related) words
            print(topics)
except:
    print('Building LDA Model...')
    lda = models.LdaModel(corpus, id2word=dictionary, random_state=RANDOM_STATE, num_topics=NUM_TOPICS, passes=NUM_PASSES)
    print('Done!')
    print('Counting Topics...')
    topics = lda.print_topics(10) # Topic ~ set of (related) words
    print(topics)

# ??? Topics Count
# print('Counting Topics...')
# lda.print_topics(10) # Topic ~ set of (related) words



# Save Model Structures
lda.save(LDA_BACKUP)
with open(DICT_BACKUP, "wb") as fp:
    pickle.dump(dictionary, fp)
fp.close()
with open(CORPUS_BACKUP, "wb") as fp:
    pickle.dump(corpus, fp)
fp.close()
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