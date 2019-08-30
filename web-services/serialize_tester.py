import os
from gensim import utils, corpora, models
import json
from content import Content
import utils
import pickle


DATABASE_FILE = 'data/wiki_content.db'
LDA_BACKUP    = 'data/lda_model'
LSI_BACKUP    = 'data/lsi_model'
DICT_BACKUP   = 'data/dictionary'
CORPUS_BACKUP = 'data/corpus'


# Content
DATABASE = utils.get_file_path(DATABASE_FILE)
content = Content(DATABASE)

# print( help( corpora.dictionary ) )

# LOAD: Dictionary
dict_file = utils.get_file_path(DICT_BACKUP)
# print('Dictionary file = {}'.format(dict_file))
# # dictionary = corpora.Dictionary(content.get_cleaned_pages())

# # with open(dict_file, "w+") as dict_file:
# # corpora.dictionary.Dictionary.save(dictionary, dict_file)
# # dictionary.save_as_text(dict_file)
dictionary = corpora.dictionary.Dictionary.load(dict_file)
# # dictionary = corpora.dictionary.load_from_text(dict_file)

# Corpus
corpus_file = utils.get_file_path(CORPUS_BACKUP)
# utils.build_corpus(dictionary, content, True, CORPUS_BACKUP)
# corpus = [dictionary.doc2bow(text) for text in content] # doc-to-bag_of_words
# utils.pickle_save(corpus_file, corpus)

corpus = pickle.load( open( corpus_file, "rb" ) )


print('Dictionary Size = {}'.format(len(dictionary)))
print('Corpus Size = {}'.format(len(corpus)))

