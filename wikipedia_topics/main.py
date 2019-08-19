#!/usr/bin/env python3
# Imports and Config
# #########################
import os
import sqlite3
import string
import logging 
import pickle 

from gensim import corpora, utils, models, similarities # "fast" vector space modeling
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
page_ids = content.get_page_ids()
page = content.get_page_by_id(page_ids[0])
print(page)

# # Lemmatize Document
# page = lemma.lemmatize(page)

