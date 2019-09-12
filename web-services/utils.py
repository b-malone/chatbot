import os, sys, string, json
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import similarities
import modeling
import config as cfg

lemma = WordNetLemmatizer()
punctuation = set(string.punctuation)
stop_words = set(stopwords.words('english'))


def print_exception_details(what, exc):
    print('Error: {}'.format(what))
    print(exc)

def variable_is_defined(var):
    return 'var' in vars() or 'var' in globals()

def debug_print(what, data):
    print("###################")
    print( what+' of type {}'.format(type(what)) )
    print( data )
    print("###################")

def get_similarity(model, corpus, q_vec):
    """
    Find related Documents.
    """
    index = similarities.MatrixSimilarity(model[corpus])
    sims = index[q_vec]
    return sims

def get_file_path(rel_filepath):
    script_path = os.path.abspath(__file__)
    script_dir  = os.path.split(script_path)[0]
    abs_file_path = os.path.join(script_dir, rel_filepath)

    return abs_file_path

def remove_punctuation(text):
    return ''.join(char for char in text if char not in punctuation)

def remove_numbers(text):
    return ''.join(char for char in text if not char.isdigit())

def remove_stop_words(text):
    return ' '.join([word for word in text.split() if word not in stop_words])

def remove_single_characters(text):
    return ' '.join([word for word in text.split() if len(word) > 1])

def lemmatize(text):
    return ' '.join([lemma.lemmatize(word) for word in text.split()])

def pickle_save(PATH, data):
    with open(PATH, "wb") as fp:
        pickle.dump(data, fp)
    fp.close()

def try_to_open_file(path):
    """
    Returns IF it's safe to open file in application.
    TRUE IFF file exists and is openable,
    FALSE otherwise
    """
    # file_exists = True
    try:
        f = open(path)
        f.close()
        return True
    except FileNotFoundError:
        # file_exists = False
        return False
    # return file_exists

# def get_top_topics(limit, topic_details):
#     """
#     Sorts and filters the topic_details from the model to the top (limit)
#     topic details.
#     """
#     topic_details_as_string = str('{}'.format(topic_details))
#     topic_dict = dict()
#     # FIND MAX (3) CONFIDENCE VALUES.
#     # FILL top_three_topics ONLY WITH THE TOPICS 
#     # THAT HAVE THE (3) HIGHEST CONFIDENCE VALUES.

#     # Destructure topic details into a map of confidence-to-TopicDetails
#     for topic_rating in topic_details_as_string.split('+'):
#         confidence = float(topic_rating.split('*')[0])
#         topic = topic_rating.split('*')[1]
#         topic_dict[confidence] = topic_rating

#     # Sort topic_dict dict BY key (confidence)
#     # Now, top_three_topics = first three topic_ratings
#     results = list(sorted(topic_dict.items()))[0:limit]
    # return dict(results)

def get_cleaned_text(text):
    text = text.replace('\n', '')
    text = remove_numbers(text)
    text = remove_stop_words(text)
    text = remove_punctuation(text)
    text = remove_single_characters(text)

    # Lemmatize the Document
    text = lemmatize(text)
    return text

def model_switch_dict():
    return {
        'lda': modeling.build_lda_model,
        'lsi': modeling.build_lsi_model,
        'tfid': modeling.build_tfid_model
    }

# def build_model(dictionary, corpus, config, should_rebuild, BACKUP_FILE):
def build_model(dictionary, corpus, should_rebuild):
    try:
        model_build_fn = model_switch_dict()[cfg.MODEL_NAME]

        return model_build_fn(dictionary, corpus, should_rebuild)
    except Exception as exc:
        print_exception_details('Building Model', exc)


def get_unique_matrix_similarity_values(sims, content, page_ids):
    pids = []
    index = 0
    result = 10

    # REFINEMENT: Possible to get "top 3-5" recommendations for pages
    #   based on "confidence" of passed in topic_details?


    while result > 0:
        page_ids_index = sims[index][0]
        page_id = page_ids[page_ids_index][0]
     
        if [page_id] not in pids:
            pids.append(page_id)
            # print('Page ID: {}'.format(page_id))
            # print('URL: {}'.format(content.get_page_url_by_id(page_id)))
            result -= 1
        index += 1
    
    return pids

    