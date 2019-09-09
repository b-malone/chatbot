#!/usr/bin/env python3
import sqlite3
import wptools  # WikiPage Tools lib
import re
from bs4 import BeautifulSoup

import utils

class HelpContent:
    def __init__(self, db_file):
        """ 
        Initialize the content class for getting data from Online Help.
        Setup a small SQLite DB in file.
        """        
        # Create DB
        self.conn = sqlite3.connect(db_file)
        cursor = self.conn.cursor()
        # Create Table for Pages
        cursor.execute('CREATE TABLE IF NOT EXISTS help_content \
            (title text, hash text, url text, content text)')  
        self.conn.commit()
        self.cursor = self.conn.cursor()


    def save_page_content(self, title, path_hash, url, text_content):
        # CLEAN: remove HTML syntax and <ref>
        text = BeautifulSoup(text_content, 'html.parser').get_text()
        # CLEAN: remove markup such as [[...]] and {{...}}
        clean_text = re.sub(r'\s*{.*}\s*|\s*[.*]\s*', '', text)

        self.cursor.execute('INSERT INTO help_content VALUES (?, ?, ?, ?)', (title, path_hash, url, clean_text))
        self.conn.commit()

    def get_page_urls(self):
        return []

    def get_page_hashes(self):
        return []

    def get_page_by_hash(self, hashKey):
        return []

    def get_cleaned_pages(self):
        pages = list()

        # for pageid in self.get_page_ids():
        #     page_id = pageid[0]
        #     page_content = self.get_page_by_id(page_id)
        #     clean_text = utils.get_cleaned_text(page_content).split()
        #     pages.append(clean_text)

        return pages

    def __iter__(self):
        """
        Iterator for the document set stored in the DB.
        """
        for clean_text in self.get_cleaned_pages():
            yield clean_text