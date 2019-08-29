#!/usr/bin/env python3

import os
from get_wikipedia_content import CrawlWikipedia
# from get_cnet_help_content import CollegeNetHelpSpider

DATABASE_FILE=os.path.abspath('data/wiki_content.db')

# 1 - Wikipedia Crawler
CATEGORY='Category:Artificial_intelligence'
PAGE_LINK_DEPTH=2

crawler = CrawlWikipedia(DATABASE_FILE)
crawler.get_categories_and_members(CATEGORY, PAGE_LINK_DEPTH)

# 2 - CollegeNet Help Crawler
# DATABASE_FILE=os.path.abspath('data/help_content.db')
# crawler = CollegeNetHelpSpider(DATABASE_FILE)
# crawler.get_categories_and_members(CATEGORY, PAGE_LINK_DEPTH)
