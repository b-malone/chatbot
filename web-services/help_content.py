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
        # Create Table for Pages
        # self.conn.cursor().execute('CREATE TABLE IF NOT EXISTS help_content \
        #     (title text, hash text, url text, content text)')  
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
        return [url for url in self.cursor.execute('SELECT url FROM help_content').fetchall()]

    def get_page_hashes(self):
        return [h for h in self.cursor.execute('SELECT hash FROM help_content').fetchall()]
        
    def get_page_ids(self):
        """
        URL Hashes are "Page_Ids" for Help Content pages.
        """ 
        return [pid for pid in self.cursor.execute('SELECT hash FROM help_content').fetchall()]

    def get_page_url_by_id(self, pid):
        query="""
            SELECT url FROM help_content WHERE hash = "{}"
        """.format(pid)
        return [pid for pid in self.cursor.execute( query ).fetchone()]

    def get_page_by_hash(self, hashKey):
        return str(self.cursor.execute('SELECT content FROM help_content WHERE hash=?', [hashKey]).fetchone())

    def get_cleaned_pages(self):
        pages = list()

        for page_hash in self.get_page_hashes():
            # page_id = pageid[0]
            # print("###################")
            # print('page_hash={}'.format(page_hash))
            page_content = self.get_page_by_hash(page_hash[0])
            clean_text = utils.get_cleaned_text(page_content).split()
            pages.append(clean_text)

        return pages

    def __iter__(self):
        """
        Iterator for the document set stored in the DB.
        """
        for clean_text in self.get_cleaned_pages():
            yield clean_text