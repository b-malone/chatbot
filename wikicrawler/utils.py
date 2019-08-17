import string
from mltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

lemma = WordNetLemmatizer()
punctuation = set(string.punctuation)
stoplist = set(stopwords.words('english'))

def remove_punctuation(text):
    return ''.join(char for char in text if char not in punctuation)

def remove_numbers(text):
    return ''.join(char for char in text if char not in char.is_digit())

def remove_stop_words(text):
    return ' '.join([word for word in text.split() word not in stoplist])

def remove_single_characters(text):
    return ' '.join([word for word in text.split() if len(word) > 1])

def lemmatize(text):
    return ' '.join([lemma.lemmatize(word) for word in text.split()])


def get_cleaned_text(tet):
    text = text.replace('\n', '')
    text = remove_numbers(text)
    text = remove_stop_words(text)
    text = remove_punctuation(text)
    text = remove_single_characters(text)

    # Lemmatize the Document
    text = lemmatize(text)
    return text

