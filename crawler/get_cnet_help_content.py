#!/usr/bin/env python3

# python -m scrapy runspidercrawler/get_cnet_help_content.py
# docker run -p 8050:8050 scrapinghub/splash

import os
import sqlite3
import scrapy
import json
import base64
# import csv
# from selenium import webdriver
# from scrapy.http import FormRequest, Request
from scrapy_splash import SplashRequest
from scrapy.selector import HtmlXPathSelector 
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


script = """
function main(splash)
  splash:init_cookies(splash.args.cookies)
  assert(splash:go{
    splash.args.url,
    headers=splash.args.headers,
    http_method=splash.args.http_method,
    body=splash.args.body,
    })
  assert(splash:wait(0.5))

  local entries = splash:history()
  local last_response = entries[#entries].response
  return {
    url = splash:url(),
    headers = last_response.headers,
    http_status = last_response.status,
    cookies = splash:get_cookies(),
    html = splash:html(),
  }
end
# """



DATABASE_FILE = 'data/help_content.db'

def get_file_path(rel_filepath):
    script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
    script_dir  = os.path.split(script_path)[0] #i.e. /path/to/dir/
    abs_file_path = os.path.join(script_dir, rel_filepath)

    return abs_file_path


# class HelpSpider(scrapy.Spider):

#     def start_requests(self):
#         login_page = 'https://25live.collegenet.com/burnside/scheduling.html#/login'

#         splash_args = {
#             'html': 1,
#             'png': 1,
#             'width': 600,
#             'render_all': 1,
#         }
#         yield SplashRequest(login_page, self.parse_result, endpoint='render.json', args=splash_args)

#     # ...
#     def parse_result(self, response):
#         # magic responses are turned ON by default,
#         # so the result under 'html' key is available as response.body
#         html = response.body

#         # you can also query the html result as usual
#         title = response.css('title').extract_first()

#         # full decoded JSON data is available as response.data:
#         png_bytes = base64.b64decode(response.data['png'])

#         # ...


class CollegeNetHelpSpider(scrapy.Spider):
    name = "collegenet_help_spider"
    start_urls = [
        'https://25live.collegenet.com/burnside/scheduling.html#/help/home'
    ]

    def start_requests(self):
        # login_page = 'https://25live.collegenet.com/burnside/scheduling.html#/auth'
        login_page = 'http://www.stackoverflow.com'
        splash_args = {
            'html': 1,
            'png': 1,
            'width': 600,
            'render_all': 1,
        }
        yield SplashRequest(login_page, self.parse_result, endpoint='execute', magic_response=True, args=splash_args)
#         driver = webdriver.PhantomJS() # Firefox(executable_path="/usr/local/bin") # PhantomJS() ( executable_path=r"usr/bin/geckodriver.exe" )
#         driver.get(self.login_page)

#         driver.find_element_by_id("loginUsername").send_keys("r25admin")
#         driver.find_element_by_id("passwloginPasswordord").send_keys("r25admin")

#         driver.find_element_by_name("submit").click()

#         driver.save_screenshot("test.png")
#         WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.LINK_TEXT, "See Available Locations")))

#         cookies = driver.get_cookies()
#         driver.close()

#         yield scrapy.Request('https://25live.collegenet.com/burnside/scheduling.html#/help/home', cookies=cookies, callback=self.parse)


    def parse_result(self, response):
        # magic responses are turned ON by default,
        # so the result under 'html' key is available as response.body
        html = response.body

        # you can also query the html result as usual
        title = response.css('#d25').extract_first()

        # full decoded JSON data is available as response.data:
        png_bytes = base64.b64decode(response.data['png'])



# #    def start_requests(self):
# #         """
# #             Handle Sessions and Authentication for crawling CollegeNET pages.
# #         """
# #         post_url = 'https://25live.collegenet.com/burnside/scheduling.html#/login'
# #         post_data = 'foo=bar'
# #         yield SplashRequest(post_url, self.parse, endpoint='execute',
# #                             magic_response=True, meta={'handle_httpstatus_all': True},
# #                             args={'lua_source': self.lua_script, 'http_method': 'POST', 'body': post_data})

#     def __init__(self):
#         """ 
#         Initialize the crawler class for getting data from Wikipedia.
#         Setup a small SQLite DB in file.

#             Pages are links off an index page.
#         """        
#         # self.driver = webdriver.Firefox()
#         self.driver = webdriver.PhantomJS()

#         # Create DB to store crawled data
#         # db_file = get_file_path(DATABASE_FILE)
#         # print('Use DB file {}'.format(db_file))
#         # self.conn = sqlite3.connect(db_file)
#         # cursor = self.conn.cursor()
#         # # # Create Table for Pages
#         # cursor.execute('CREATE TABLE IF NOT EXISTS help_content (pageid text, category text, url text, content text)')    
#         # self.conn.commit()
#         # self.cursor = self.conn.cursor()


#     # def parse(self, response):
#     #     for title in response.css('.post-header>h2'):
#     #         yield {'title': title.css('a ::text').get()}

#     #     for next_page in response.css('a.next-posts-link'):
#     #         yield response.follow(next_page, self.parse)

#     #  # Parse through each Start URLs
#     # def start_requests(self):
#     #     for url in self.start_urls:
#     #         yield scrapy.Request(url=url, callback=self.parse) 

#     # Parse function: Scrape the webpage and store it
#     def parse(self, response):
#         HELP_PAGE_LINK_SELECTOR = '#help-default-topics a'
#         HELP_TOPIC_SELECTOR = '.topic'

#         self.driver.get(response.url)

#         if "See Available Locations" in response.body:
#             self.log("Login successful")
#         else:
#             self.log("Login failed")

#         # # Output filename
#         # filename = "angular_data.csv"
#         # with open(filename, 'a+') as f:
#         #     writer = csv.writer(f)
#         #     # Selector for all the names from the link with class 'ng-binding'
#         #     names = self.driver.find_elements_by_css_selector("a.ng-binding")
#         #     for name in names:
#         #         title = name.text
#         #         writer.writerow([title])
#         # self.log('Saved file %s' % filename)


#         # # Pull Help Page Data
#         # for topic in self.driver.find_elements_by_css_selector(HELP_TOPIC_SELECTOR):
#         #     NAME_SELECTOR = 'h1 ::text'
#         #     yield {
#         #         'title': topic.css(NAME_SELECTOR).extract_first(),
#         #     }

#         # # Follow Links to Help Pages...
#         # for next_page in self.driver.find_elements_by_css_selector(HELP_PAGE_LINK_SELECTOR):
#         #     yield response.follow(next_page, self.parse)

        


