#!/usr/bin/env python3

import os
from get_wikipedia_content import CrawlWikipedia

DATABASE_FILE=os.path.abspath('data/wiki_content.db')

CATEGORY='Category:Artificial_intelligence'
PAGE_LINK_DEPTH=1

crawler = CrawlWikipedia(DATABASE_FILE)
crawler.get_categories_and_members(CATEGORY, PAGE_LINK_DEPTH)
