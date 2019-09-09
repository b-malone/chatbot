# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
import logging
import base64
import json
import os
import re
from bs4 import BeautifulSoup
import sqlite3

def get_file_path(rel_filepath):
    script_path = os.path.abspath(__file__) 
    script_dir  = os.path.split(script_path)[0] 
    abs_file_path = os.path.join(script_dir, rel_filepath)

    return abs_file_path

filepath = __file__ + '/../../../../../../web-services/data/help.db';
print( 'data_path={}'.format(os.path.abspath( filepath ) ) )
# print( 'PATH = {}'.format(get_file_path(filepath)) )