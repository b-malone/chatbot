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
# CMD gunicorn app:app -b0.0.0.0:5000
RUN python init_nltk.py
# CMD [ "start.py" ]
CMD gunicorn app:app -b0.0.0.0:5000

# FROM ubuntu:16.04

# RUN apt-get update -y && \
#     apt-get install -y python3-pip python-dev build-essential libssl-dev libffi-dev

# # We copy just the requirements.txt first to leverage Docker cache
# # COPY ./requirements.txt /app/requirements.txt
# COPY . /app

# WORKDIR /app

# RUN pip3 install -r requirements.txt

# # COPY . /app

# ENTRYPOINT [ "python3" ]
# CMD [ "app.py" ]