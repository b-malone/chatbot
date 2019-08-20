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
NUM_TOPICS=100
RANDOM_STATE=1
# ### LOGGING for Gensim
logging.basicConfig()
# ### Data Stores and backups
DATABASE_FILE = 'data/wiki_content.db'
LDA_BACKUP = '../data/lda_model'
DICT_BACKUP = '../data/dictionary'
CORPUS_BACKUP = '../data/corpus'

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

# EX: View a page
# page_ids = content.get_page_ids()
# page = content.get_page_by_id(page_ids[0])
# print( str(page) )
# print( type(content) )
# print('=============')

# # Lemmatize and Clean Document
# page = lemma.lemmatize(page)
pages_content = content.get_cleaned_pages()
print('=============')
print('Pages of Content: {}'.format(len(pages_content)))
# print('Which is OfType: {}'.format( type(pages_content) ))
print('=============')

# for i in range(5):
#     cursor = pages_content[i][0]
#     obj = pages_content[i][1]
#     # count = cursor.getColumnCount()
#     # print( pages_content[i] )
#     # print( json.dumps(cursor) )

# # print( pages_content[0].fetchone() )
# print('=============')

#
# !!!!!!!!!!
# Dictionary being built wrong!
#   Needs to be built on all content! NOT just (one) page.
#   All pages' contents need to also be lammatized!
#

# dictionary = corpora.Dictionary(content)    # list: (word_id, appearance count)
# dictionary = corpora.Dictionary(pages_content)    # list: (word_id, appearance count)
# # dictionary.filter_extremes(no_below=5, no_above=0.4)
# print(dictionary)
# print(len(dictionary))
# print('=============')

# # Create a Corpus
# corpus = [dictionary.doc2bow(text) for text in content] # doc-to-bag_of_words
# print(len(corpus))

# # Build LDA Model
# lda = models.LdaModel(corpus, id2word=dictionary, random_state=RANDOM_STATE, num_topics=NUM_TOPICS, passes=NUM_PASSES)

# # ??? Topics Count
# lda.print_topics(lda) # Topic ~ set of (related) words



# Save Model Structures
# lda.save(LDA_BACKUP)
# with open(DICT_BACKUP, "wb") as fp:
#     pickle.dump(dictionary, fp)
# fp.close()
# with open(CORPUS_BACKUP, "wb") as fp:
#     pickle.dump(corpora, fp)
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