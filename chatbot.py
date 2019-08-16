import io
import random
import string
import warnings
import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import warnings
import nltk
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.tokens import Span
from spacy import displacy
from spacy.attrs import ENT_IOB, ENT_TYPE
from collections import Counter
from bs4 import BeautifulSoup
import requests
import re


# warnings.filterwarnings('ignore')

nltk.download('popular', quiet=True) # for downloading packages
# nltk.download('punkt') # first-time use only
# nltk.download('wordnet') # first-time use only
# sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
# word_tokens = nltk.word_tokenize(raw)# converts to list of words

spacy.prefer_gpu()
# python -m spacy download en, python -m spacy.en.download  
nlp = spacy.load("en_core_web_sm")

# nlp.pipe_names
# ['tagger', 'parser', 'ner']
# nlp.pipeline
# [('tagger', <spacy.pipeline.Tagger>),
# ('parser', <spacy.pipeline.DependencyParser>),
# ('ner', <spacy.pipeline.EntityRecognizer>)]

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def url_to_string(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(["script", "style", 'aside']):
        script.extract()
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))

def tags_and_lemmas(text):
    return [(x.orth_,x.pos_, x.lemma_) for x in [y 
                                for y
                                in nlp(str(text))
                                if not y.is_stop and y.pos_ != 'PUNCT']]


# nlp = spacy.load("en_core_web_sm")
# doc = nlp(u"FB is hiring a new Vice President of global policy")
# ex = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'
# doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')

# pprint([(X.text, X.label_) for X in doc.ents])

# GIST: NTLK
with open("data/help_overview.txt", "r") as f:
    sample = f.read()
     
sentences = nltk.sent_tokenize(sample)
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences] #  a way for you to remove a chunk from a chunk
chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)  # group words into hopefully meaningful chunks

def extract_entity_names(t):
    entity_names = []
    
    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
                
    return entity_names

entity_names = []
for tree in chunked_sentences:
    entity_names.extend(extract_entity_names(tree))

# Print unique entity names
print(set(entity_names))

# ######################
# Extracting named entity from an article
# ny_bb = url_to_string('https://www.nytimes.com/2018/08/13/us/politics/peter-strzok-fired-fbi.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news')
# article = nlp(ny_bb)
# print(len(article.ents))
# * unique labels for all entities
# labels = [x.label_ for x in article.ents]   # PERSON: x, ORG.: y, ...
# print(Counter(labels))

# * tagging + lemms for entities
# tagsAndLemmas = [(x.orth_,x.pos_, x.lemma_) for x in [y 
#                                       for y
#                                       in nlp(str(ny_bb))
#                                       if not y.is_stop and y.pos_ != 'PUNCT']]
# print(tagsAndLemmas)

# header = [ENT_IOB, ENT_TYPE]

# #####################
# 25Live Help
# helpFile  = open("data/help_overview.txt", "r")
# helpText = nlp(helpFile.read())
# print(len(helpText.ents))
# tagsAndLemmas = tags_and_lemmas(helpText)
# print(tagsAndLemmas)
