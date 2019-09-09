# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
import logging, base64, json, time, math, os, re
# import base64
# import json
# import math
# import os
# import re
from bs4 import BeautifulSoup
import sqlite3

# DEBUGGING
# scrapy shell 'http://quotes.toscrape.com/'

# ToDo
# ### (Docker + Flask + SQLite) "Flask with sqlite3"
# https://github.com/mromadisiregar/docker/tree/master/flask-sqlite3

# python -m scrapy runspider scrapy-splash/example/scrashtest/spiders/test.py

class HelpSpider(scrapy.Spider):
    """
        A Scrapy-Splash web crawling spider for pulling CollegeNET Online Help
        documentation content for use in Topic Modeling and a ChatBot.
        
        Bringing intelligent software and information to the people, one line 
        of Python at a time.

        Attributes
        ----------
        number_of_legs: err, this isn't a real spider

        custom_settings: splash plugin specific settings for running a docker container
            to pull requset responses into for interaction and spidering.
            Running on a local machine near you @ http://0.0.0.0:8050

        visit_help_page_script: requests are basically bundled HTTP requests that include
            the interaction script for splash to run together. If you're doing something 
            like visiting 30+ links to grab content, the Scrapy requests will timeout.
            Therefore, this function is basically a temmplate for visiting each link
            so it can be run in a somewhat async loop to (1) avoid timeoutes, and 
            (2) accompling visiting every page in one scrape.
        
        start_requests: this function runs at the beginning of all Spider runs. Current
            functionality includes authenticating into the internal app/tool, and then
            visiting the index page of links where we want to start crawling.
    """

    name = "help"
    allowed_domains = ["25live.collegenet.com"]
    start_urls = [
        'https://25live.collegenet.com/burnside/scheduling.html',
        'https://25live.collegenet.com/burnside/scheduling.html#/help/home'
    ]

    # Lets Scrapy-Splash pull HTTP request responses into a Docker container
    # and interact on the page with splash and JS as-if Selenium/Webdriver.
    custom_settings = {
        'SPLASH_URL': 'http://localhost:8050',
        # if installed Docker Toolbox: 
        #  'SPLASH_URL': 'http://192.168.99.100:8050',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    }


    debug_script="""
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(3))

        splash:set_viewport_full()
        -- splash.response_body_enabled = true

        -- Login to 25Live (Scheduling)
        local name_input = splash:select('input[name=username]')   
        name_input:send_text("r25admin")
        local pass_input = splash:select('input[name=password]')
        pass_input:send_text("r25admin")
        assert(splash:wait(1))
        local submit_button = assert(splash:select('form[name="login"] button'))
        submit_button:click()

        assert(splash:wait(5))
        
        -- Navigate to Help Index Page
        local help_link = splash:select('a[href="#/help"]')
        help_link:click()
        
        assert(splash:wait(5))

        local elementIsVisible = function(sel)
            local js = string.format([[
                document.querySelector("%s") === null;
            ]], sel)
            return splash:evaljs(js)
        end

        local getUrlHash = function()
            local js = 'window.location.hash'
            return splash:evaljs(js)
        end

        local isHelpIndexPage = function()
            return getUrlHash() == '#/help/home'
        end

        --splash:set_viewport_full()
        --splash.response_body_enabled = true

        --local search_input = splash:select('input[name=username]')   
        --search_input:send_text("r25admin")
        --local search_input = splash:select('input[name=password]')
        --search_input:send_text("r25admin")
        --assert(splash:wait(1))
        --local submit_button = assert(splash:select('form[name="login"] button'))
        --submit_button:click()

        --assert(splash:wait(3))

        local title = "TEST"
        return {
            title_is_visible = elementIsVisible("h1.title"),
            is_help_index = isHelpIndexPage(),
            title = title,
            url = splash:url()
        }
    end
    """

    # Returns a list of Help Page links to visit in a loop and pull content.
    burnside_help_script="""
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(3))

        splash:set_viewport_full()
        -- splash.response_body_enabled = true

        -- Login to 25Live (Scheduling)
        local name_input = splash:select('input[name=username]')   
        name_input:send_text("r25admin")
        local pass_input = splash:select('input[name=password]')
        pass_input:send_text("r25admin")
        assert(splash:wait(1))
        local submit_button = assert(splash:select('form[name="login"] button'))
        submit_button:click()

        assert(splash:wait(5))
        
        -- Navigate to Help Index Page
        local help_link = splash:select('a[href="#/help"]')
        help_link:click()
        
        assert(splash:wait(5))
        
        local help_index_url = splash:url()

        local countHelpTopicPageLinks = function(sel)
            local js = string.format([[
            var el = document.querySelectorAll("%s");
                el.length;
            ]], sel)
            return splash:evaljs(js)
        end

        local num_links = countHelpTopicPageLinks("#help-default-topics a")

  
        return {
            -- html = splash:html(),
            -- png = splash:png(),
            -- har = splash:har(),
            index_url =  help_index_url,
            url = splash:url(),
            count = num_links
        }
    end
    """

    def __init__(self):
        # Create DB
        # __file__ + '/../../../../../../web-services/data'
        # db_file = self.get_file_path('pages/help/help.db')
        db_file = os.path.abspath( __file__ + '/../../../../../../web-services/data/help.db' )
        # db_file = self.get_file_path( data_file_path )
        self.conn = sqlite3.connect(db_file)
        cursor = self.conn.cursor()
        # Create Table for Pages
        cursor.execute('CREATE TABLE IF NOT EXISTS help_content \
            (title text, hash text, url text, content text)')  
        self.conn.commit()
        self.cursor = self.conn.cursor()


    def visit_help_page_script(self, i, index_url):
        return_attrs = """{
            hash = hash,
            title = title,
            url = topic_page_url,
            content = text
        }"""
        _script_a = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(3))

            splash:set_viewport_full()
            splash.response_body_enabled = true
            -- splash.private_mode_enabled = false

            local search_input = splash:select('input[name=username]')   
            search_input:send_text("r25admin")
            local search_input = splash:select('input[name=password]')
            search_input:send_text("r25admin")
            assert(splash:wait(1))
            local submit_button = assert(splash:select('form[name="login"] button'))
            submit_button:click()

            assert(splash:wait(3))
            
            local help_link = splash:select('a[href="#/help"]')
            help_link:click()
            
            assert(splash:wait(5))
            
            local help_index_link = splash:url()
            
            local elementIsVisible = function(sel)
                local js = string.format([[
                    document.querySelector("%s") === null;
                ]], sel)
                return splash:evaljs(js)
            end

            local getTextContent = function(sel)
                local js = string.format([[
                    var el = document.querySelector("%s");
                    el.textContent;
                ]], sel)
                return splash:evaljs(js)
            end

            local countHelpTopicPageLinks = function(sel)
                local js = string.format([[
                var el = document.querySelectorAll("%s");
                el.length;
                ]], sel)
                return splash:evaljs(js)
            end

            local getUrlHash = function(sel)
                local js = 'window.location.hash';
                return splash:evaljs(js);
            end
        """

        _script_b = """
             -- Visit each Help Topic Page...
            splash:runjs('document.querySelectorAll("#help-default-topics a")[{}].click()')
            assert(splash:wait(3))

            --local num_links = countHelpTopicPageLinks("#help-default-topics a")
            -- * Get Topic Page Title
            local title = ''
            local text  = ''
            local topic_page_url = ''
            if elementIsVisible("h1.title") then title = getTextContent("h1.title")
            else title = splash:url()
            end

            if elementIsVisible(".help-item") then title = getTextContent(".help-item")
            else title = splash:url()
            end

            --title = getTextContent("h1.title")
            --text = getTextContent(".help-item")
            topic_page_url = splash:url()

            -- "Reset" Navigation to Help Index Page
            local help_index_url = "{}"
            local hash = getUrlHash()

            assert(splash:go(help_index_url))
            assert(splash:wait(3))

            return {}
        end
        """.format(i, index_url, return_attrs)

        return _script_a + _script_b

    def start_requests(self):
        yield SplashRequest(
            self.start_urls[0], 
            self.parse,
            endpoint='execute',
            args={
                'html': 1,
                'wait': 3,
                'lua_source': self.burnside_help_script,
                'timeout': 90
            },
        )


    def parse(self, response):
        logger = logging.getLogger()
        data = response.data

        n = data['count']
        # Avoiding TimeOut Errors:
        # indexes = range(n)
        indexes = range(n)[-3:-1]
        # scrape 1 - range = range(n)[0:math.floor(n/2)]
        # indexes = range(n)[0:math.floor(n/2)]
        # scrape 2 - range = range(n)[math.floor(n/2):-1]
        # indexes = range(n)[math.floor(n/2):-1]
        for i in indexes:
            # Visit Help Page #i
            # *** Starting from Help Index Page EACH loop
                # (includes "reset" of navigation to the help index page inside script)
            help_page_script = self.visit_help_page_script(i, data['index_url'])

            yield SplashRequest(
                self.start_urls[0],
                # data['index_url'],
                self.parse_help_page,
                endpoint="execute",
                args={"lua_source": help_page_script},
                # args={"lua_source": self.debug_script},
                dont_filter=True
            )
            time.sleep(2)
            

        # logger.warning("####################")
        
    
    def get_file_path(self, rel_filepath):
        script_path = os.path.abspath(__file__) 
        script_dir  = os.path.split(script_path)[0] 
        abs_file_path = os.path.join(script_dir, rel_filepath)

        return abs_file_path
  
    def save_page_content(self, title, path_hash, url, text_content):
        # CLEAN: remove HTML syntax and <ref>
        text = BeautifulSoup(text_content, 'html.parser').get_text()
        # CLEAN: remove markup such as [[...]] and {{...}}
        clean_text = re.sub(r'\s*{.*}\s*|\s*[.*]\s*', '', text)

        self.cursor.execute('INSERT INTO help_content VALUES (?, ?, ?, ?)', (title, path_hash, url, clean_text))
        self.conn.commit()

    def parse_help_page(self, response):
        logger = logging.getLogger()

        logger.warning("####################")

        logger.warning(response.data['hash'])
        # logger.warning( list(response.data.keys()) )

        # try:
        #     logger.warning(response.data['title'])
        # except:
        #     logger.warning("NO TITLE PROP")

        # try:
        #     logger.warning(response.data['hash'])
        # except:
        #     logger.warning("NO hash PROP")

        # Dump JSON data returned from scrape to file
        # hash_last = response.data['hash'].split("/")
        # filepath = self.get_file_path('pages/help/{}.json'.format(hash_last[-1]))
        # with open(filepath, 'w+') as outfile:
        #     json.dump(response.data, outfile)

        # Store scraped (JSON) data to SQLite DB
        self.save_page_content(response.data['title'], response.data['hash'], response.data['url'], response.data['content'])

        logger.warning("####################")


    def parse_debug(self, response):
        logger = logging.getLogger()

        logger.warning("####################")

        # DEBUG: List Keys of "response.data"
        logger.warning( type(response.data) )
        logger.warning( list(response.data.keys()) )
        # try:
        #     logger.warning(response.data['title'])
        # except:
        #     logger.warning("NO TITLE PROP")

        # try:
        #     logger.warning(response.data['url'])
        # except:
        #     logger.warning("NO url PROP")

        logger.warning("####################")