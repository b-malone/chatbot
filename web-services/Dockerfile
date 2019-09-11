# FROM python:3
# WORKDIR /usr/src/app
# COPY requirements.txt .
# RUN pip3 install --no-cache-dir -r requirements.txt
# # COPY ./web-services /usr/src/app

# ENTRYPOINT ["python"]
# RUN python -m nltk.downloader stopwords

# CMD ["topics_service.py"]

FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev build-essential libssl-dev libffi-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

# COPY . /app

ENTRYPOINT [ "python3" ]
CMD [ "topics_service.py" ]