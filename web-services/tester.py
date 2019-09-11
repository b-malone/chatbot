import os, json, pickle
from gensim import corpora, models
import help_content
import utils
import inspect
import config as cfg


# query = "how do I schedule an event?"
query = "What is the purpose of 25Live Event Wizard?"

# ### Content ###
DATABASE = utils.get_file_path(cfg.DATABASE_FILE)
content = help_content.HelpContent(DATABASE)

# print( help( corpora.dictionary ) )
should_rebuild = False

# ### Dictionary ###
dict_file = utils.get_file_path(cfg.DICT_BACKUP)
# dictionary = corpora.dictionary.Dictionary.load(dict_file)
dictionary = utils.build_dictionary(content, should_rebuild, cfg.DICT_BACKUP)

# ### Corpus ###
corpus_file = utils.get_file_path(cfg.CORPUS_BACKUP)
# utils.pickle_save(corpus_file, corpus)
# corpus = corpora.MmCorpus(corpus_file)
corpus = utils.build_corpus(dictionary, content, should_rebuild, cfg.CORPUS_BACKUP)
# corpus = pickle.load( open( corpus_file, "rb" ) )

# print( cfg.MODEL_NAME )

# ### LDA Model ###
bow = dictionary.doc2bow(utils.get_cleaned_text( query.lower() ).split())
# bag_of_words = [word for word in bow]
model = utils.build_model(dictionary, corpus, should_rebuild)
q_vec = model[bow]    # "query vector"
# topic_details = list()
topic_details = model.print_topic( max(q_vec, key=lambda item: item[1])[0] )



print('Dictionary Size = {}'.format(len(dictionary)))
print('Corpus Size = {}'.format(len(corpus)))
print('Topic Details: ')
print( topic_details )
