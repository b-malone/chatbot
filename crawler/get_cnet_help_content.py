#!/usr/bin/env python3

import sqlite3
import scrapy
import re
# from bs4 import BeautifulSoup

# $ scrapy runspider [scraper.py]

class CollegeNetHelpSpider(scrapy.Spider):
    name = "collegenet_help_spider"
    start_urls = ['https://25live.collegenet.com/burnside/scheduling.html#/help/home']

    def __init__(self, db_file):
        """ 
        Initialize the crawler class for getting data from Wikipedia.
        Setup a small SQLite DB in file.

            Pages are links off an index page.
        """        
        # self.categories = []

        # # Create DB
        # print('Use DB file {}'.format(db_file))
        # self.conn = sqlite3.connect(db_file)
        # cursor = self.conn.cursor()
        # # Create Table for Pages
        # cursor.execute('CREATE TABLE IF NOT EXISTS content (pageid text, category text, url text, content text)')    
        # self.conn.commit()
        # self.cursor = self.conn.cursor()
    # def parse(self, response):
    #     for title in response.css('.post-header>h2'):
    #         yield {'title': title.css('a ::text').get()}

    #     for next_page in response.css('a.next-posts-link'):
    #         yield response.follow(next_page, self.parse)

    def parse(self, response):
        HELP_PAGE_LINK_SELECTOR = '#help-default-topics a'
        HELP_TOPIC_SELECTOR = '.topic'
        # for brickset in response.css(SET_SELECTOR):
        #     pass

        # Pull Help Page Data
        for topic in response.css(HELP_TOPIC_SELECTOR):
            NAME_SELECTOR = 'h1 ::text'
            yield {
                'title': topic.css(NAME_SELECTOR).extract_first(),
            }

        # Follow Links to Help Pages...
        for next_page in response.css(HELP_PAGE_LINK_SELECTOR):
            yield response.follow(next_page, self.parse)

        


