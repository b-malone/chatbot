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
      -- docker-compose build
      -- docker-compose up
      -- http://localhost:5000

# Usage



# Issues
 - pycurl and openssl: 
    -- https://github.com/transloadit/python-sdk/issues/4
    -- https://cscheng.info/2018/01/26/installing-pycurl-on-macos-high-sierra.html