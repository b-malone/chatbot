import os
import string
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

lemma = WordNetLemmatizer()
punctuation = set(string.punctuation)
stoplist = set(stopwords.words('english'))

def get_file_path(rel_filepath):
    dir_path = os.path.split( os.path.dirname(__file__) )
    # path = os.path.abspath( os.path.relpath(rel_filepath) )
    path = os.path.join(dir_path[0], rel_filepath)
    print('path = {}'.format(path))
    # return os.path.join(path, rel_filepath)
    return path

def remove_punctuation(text):
    return ''.join(char for char in text if char not in punctuation)

def remove_numbers(text):
    return ''.join(char for char in text if char not in char.is_digit())

def remove_stop_words(text):
    return ' '.join([word for word in text.split() if word not in stoplist])

def remove_single_characters(text):
    return ' '.join([word for word in text.split() if len(word) > 1])

def lemmatize(text):
    return ' '.join([lemma.lemmatize(word) for word in text.split()])


def get_cleaned_text(text):
    text = text.replace('\n', '')
    text = remove_numbers(text)
    text = remove_stop_words(text)
    text = remove_punctuation(text)
    text = remove_single_characters(text)

    # Lemmatize the Document
    text = lemmatize(text)
    return text


def get_unique_matrix_sim_values(sims, page_ids):
    pids = []
    index = 0
    result = 10

    while result > 0:
        page_id = page_ids[sims[index][0]]
        if page_id not in pids:
            pids.append(page_id)
            # print('Page ID {}: {}'.format(page_id[0]), content.get_page_url_by_id(page_id[0]))
            result -= 1
        index += 1
    
    return pids