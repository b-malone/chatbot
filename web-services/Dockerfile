FROM python:3.7.1-stretch

WORKDIR /app
COPY . /app

# RUN pip3 install --upgrade pip3
RUN pip3 install -r requirements.txt

# import nltk
# from nltk.stem.wordnet import WordNetLemmatizer
# from nltk.corpus import stopwords
# nltk.download('stopwords')
# from nltk.corpus import wordnet
# nltk.download('wordnet')
# Init NLTK

EXPOSE 5000

RUN python init_nltk.py

CMD gunicorn app:app -b0.0.0.0:5000 
# --capture-output --log-level debug
# gunicorn --workers 3 --bind 127.0.0.1:5000 --error-logfile /app/error.log --access-logfile /app/access.log --capture-output --log-level debug
