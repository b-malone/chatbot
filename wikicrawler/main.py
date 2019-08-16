import sqlite3
import string
import logging 
import pickle 

from genism import corpora, utils, models, similarities
from collections import defaultdict

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from mltk.corpus import stopwords
nltk.download('stopwords')
from nltk.corpus import wordnet
nltk.download('wordnet')

# Configuration 
NUM_PASSES=10
NUM_TOPICS=100
RANDOM_STATE=1
# ### LOGGING for Gensim
logging.basicConfig()
# ### Data Stores and backups
DATABASE = '../data/content.db'
LDA_BACKUP = '../data/lda_model'
DICT_BACKUP = '../data/dictionary'
CORPUS_BACKUP = '../data/corpus'

