# Unsupervised Topic Modeling Tool
   A simple Python3 topic modeling tool that crawls for data and runs on the command line or as a Docker container web service (Flask application).

# Dependencies
   - Python 3
   - Docker, Docker Compose
   - (Crawling or Hookup) Data for the Content database to topic model on

# Setup
   - Clone the repo
   - $ pip3 install -r requirements.txt
   - Run the Crawler to get content for the DateBase and modeling
      -- python crawler/run_crawler.py
   - (CLI) Run the Modeling process locally:
      -- python wikipedia_topics/main.py
      -- (CLI options) --rebuild=True,False (rebuild models and structures) --model=lad,lsi (which topic modeling algorithm to use)
   - (Web Service)
      -- cd /web-services
      -- Create and Activate Python 3.7 virtual environment (with Anaconda)
         * conda create --name venv python=3.7.3
         * conda activate venv
      -- Install pip(3) packages/dependencies:
         * pip install -r requirements.txt 
      -- !!! Might need to fix PyCurl compilation issue (mentions SSL):
         * pip uninstall pycurl
         * export PYCURL_SSL_LIBRARY=openssl
         * pip install pycurl --no-cache-dir
      -- (Development) Run Flask App
         * python -m flask run
         * Endpoints at http://localhost:5000/*
      -- docker-compose build
      -- docker-compose up
      -- http://localhost:5000

# Usage
   - Crawling
      * cd into craler/scrapy-splash, build a spider
      * Run Docker container for pulling HTML content into: 
      ```
      $ docker run -p 8050:8050 scrapinghub/splash --max-timeout 3600
      ```
      * Run the scrapy-splash spider alongside the Docker container: 
      ```
      $ python -m scrapy runspider /path/to/spider.py
      ```
   - Talking to ChatBot:
      * Spin up or deploy the web-services app.py Flask application
      ```
      (Development)
      FLASK_APP=main.py FLASK_DEBUG=1 python -m flask run
      ```
      * Make POST requests to the Flask application with the payload {'query': MESSAGE}:
      ```
      curl --header "Content-Type: application/json" --request POST --data '{"query": "how do I schedule an event?"}' http://localhost:5000/topics/lda
      ```
## NOTE: The URLs need to be fixed so that one endpoint pulls chat requests and proxies them for conversation or modeling. Right now, different models are at different endpoints so the accuracy of different topic modeling algorithms can be compared (LDA is most stable):
   * LDA: http://localhost:5000/topics/lda
   * LSI: http://localhost:5000/topics/lsi
   * TFID: http://localhost:5000/topics/tfid (refines model inputs, currently broken)


# Issues
 - pycurl and openssl: 
    -- https://github.com/transloadit/python-sdk/issues/4
    -- https://cscheng.info/2018/01/26/installing-pycurl-on-macos-high-sierra.html

# Resources
## Articles and references for creating a Topic Modeling and ChatBot pipeline and improving and validating prediction accuracy
   * https://www.programcreek.com/python/example/96045/gensim.models.TfidfModel
   * https://towardsdatascience.com/unsupervised-nlp-topic-models-as-a-supervised-learning-input-cf8ee9e5cf28
   * https://textblob.readthedocs.io/en/dev/
   * https://lizadaly.com/brobot/
   * https://monkeylearn.com/topic-analysis/
