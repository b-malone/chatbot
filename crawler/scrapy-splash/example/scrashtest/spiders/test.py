# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
import logging
import base64
import json
import os
import pickle

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

        local title = "TEST"
        return {
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
        splash.response_body_enabled = true

        -- Login to 25Live (Scheduling)
        local search_input = splash:select('input[name=username]')   
        search_input:send_text("r25admin")
        local search_input = splash:select('input[name=password]')
        search_input:send_text("r25admin")
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
            html = splash:html(),
            png = splash:png(),
            har = splash:har(),
            index_url =  help_index_url,
            count = num_links
        }
    end
    """

    # scrape_help_content_script="""
    # function main(splash, args)
    #     local help_index_url = splash:url()

    #     -- Visit each Help Topic Page...
    #     splash:runjs('document.querySelectorAll("#help-default-topics a")[1].click()')
    #     assert(splash:wait(3))

    #     local getTextContent = function(sel)
    #         local js = string.format([[
    #             var el = document.querySelector("%s");
    #             el.textContent;
    #             ]], sel)
    #         return splash:evaljs(js)
    #     end

    #     -- local content = splash:runjs('document.querySelectorAll("").text()')
    #     -- * Get Topic Page Title
    #     local title = getTextContent("h1.title")
  
    #     return {
    #         html = splash:html(),
    #         png = splash:png(),
    #         har = splash:har(),
    #         url =  splash:url(),
    #         title = title
    #     }
    # end
    # """

    def visit_help_page_script(self, i, index_url):
        # "{html=splash:html(),png=splash:png(), href=href,}"
        # return_attrs = """{
        #     html = splash:html(),
        #     png = splash:png(),
        #     har = splash:har(),
        #     url =  topic_page_url,
        #     title = title
        # }"""
        # return_attrs = """{
        #     url =  topic_page_url
        # }"""
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
                local js = 'window.location.hash'
                return splash:evaljs(js)
            end
        """

        _script_b = """
             -- Visit each Help Topic Page...
            splash:runjs('document.querySelectorAll("#help-default-topics a")[{}].click()')
            assert(splash:wait(3))

            --local num_links = countHelpTopicPageLinks("#help-default-topics a")
            -- * Get Topic Page Title
            local title = getTextContent("h1.title")
            local text = getTextContent(".help-item")
            local topic_page_url = splash:url()

            -- "Reset" Navigation to Help Index Page
            local help_index_url = "{}"
            local hash = getUrlHash()

            assert(splash:go(help_index_url))
            assert(splash:wait(3))

            return {}
        end
        """.format(i, index_url, return_attrs)

        # _script_a="""
        #     function main(splash, args)
        #         -- Visit each Help Topic Page...
        #         splash:runjs('document.querySelectorAll("#help-default-topics a")[{}].click()')
        #         assert(splash:wait(3))
        # """.format(i)
        # _script_b="""
        #         local getTextContent = function(sel)
        #             local js = string.format([[
        #                 var el = document.querySelector("%s");
        #                 el.textContent;
        #                 ]], sel)
        #             return splash:evaljs(js)
        #         end
        # """
        # _script_c="""
        #         -- local content = splash:runjs('document.querySelectorAll("").text()')
        #         -- * Get Topic Page Title
        #         -- local title = getTextContent("h1.title")

        #         local topic_page_url = splash:url()

        #         -- "Reset" Navigation to Help Index Page
        #         local help_index_url = {}

        #         assert(splash:go(help_index_url))
        #         assert(splash:wait(3))

        #         return {}
        #     end
        # """.format(index_url, return_attrs)

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

        # Help Pages (Links)
        # help_links = response.links # css('a')

        data = response.data

        logger.warning("####################")
        # logger.warning("data['index_url'] = {}".format(data['index_url']))
        # logger.warning("####################")

        n = data['count']
        for i in range(n):
            # Visit Help Page #i
            # *** Starting from Help Index Page EACH loop
                # (includes "reset" of navigation to the help index page inside script)
            help_page_script = self.visit_help_page_script(i, data['index_url'])
            # filepath = self.get_file_path('scripts/script'+str(i)+'.text')
            # logger.warning( 'filepath={}'.format(filepath) )

            # logger.warning("i = {}".format(i))
            # logger.warning("####################")

            # with open(filepath, 'w+') as outfile:
            #     outfile.write( lua_script )
            #     outfile.close()
                # json.dump(outfile, lua_script)

            yield SplashRequest(
                self.start_urls[0],
                self.parse_help_page,
                endpoint="execute",
                args={"lua_source": help_page_script},
                dont_filter=True
            )

            # yield SplashRequest(response.url, self.parse_help_page,
            #     endpoint="execute",
            #     args={"lua_source": self.visit_help_page_script(i, data['index_url'])},
            #     dont_filter=True)

        # logger.warning(data['index_url'])
        # logger.warning(data['count'])

        logger.warning("####################")
        

        # le = LinkExtractor()
        # html = response._body
        # you can also query the html result as usual
        # links = response.css('a')  #  .extract_first()
        # logger.warning("####################")

        # for a in response.help_links:
        #     logger.log(item)

        # logger.warning("####################")
    
    def get_file_path(self, rel_filepath):
        script_path = os.path.abspath(__file__) 
        script_dir  = os.path.split(script_path)[0] 
        abs_file_path = os.path.join(script_dir, rel_filepath)

        return abs_file_path
  

    def parse_help_page(self, response):
        logger = logging.getLogger()
        # logger.warning(response.title)
        # logger.warning(response.url)
        # logger.info("\n")

        logger.warning("####################")

        logger.warning( type(response.data) )
        logger.warning(response.data)

        try:
            logger.warning(response.data['title'])
        except:
            logger.warning("NO TITLE PROP")

        try:
            logger.warning(response.data['hash'])
        except:
            logger.warning("NO hash PROP")

        # logger.warning(response.data.title)
        # logger.warning(response.data.url)
        hash_last = response.data['hash'].split("/")
        filepath = self.get_file_path('pages/help/{}.json'.format(hash_last[-1]))
        with open(filepath, 'w+') as outfile:
            # results = {}
            # results['title'] = response.data['title']
            # json.dump(outfile, response.data)
            json.dump(response.data, outfile)
            # pickle.dump(response.data, outfile)

        logger.warning("####################")

        # print("PARSED", response.real_url, response.url)
        # print(response.css("title").extract())
        # print(response.data["har"]["log"]["pages"])
        # print(response.headers.get('Content-Type'))
