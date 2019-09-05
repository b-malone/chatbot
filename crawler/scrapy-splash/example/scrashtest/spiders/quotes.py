# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
import logging
import base64

# DEBUGGING
# scrapy shell 'http://quotes.toscrape.com/'

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    # http_user = 'splash-user'
    # http_pass = 'splash-password'

    def parse(self, response):
        logger = logging.getLogger()

        le = LinkExtractor()

        # logger.warning("####################")
        # logger.warning(response._body)
        # logger.warning("####################")
        # print(response)

        html = response._body

        # you can also query the html result as usual
        links = response.css('a').extract_first()


        logger.warning("####################")
        logger.warning(links)
        logger.warning("####################")

        # full decoded JSON data is available as response.data:
        # png_bytes = base64.b64decode(response.data['png'])

        # for link in le.extract_links(response._body):
        #     yield SplashRequest(
        #         link.url,
        #         self.parse_link,
        #         endpoint='render.json',
        #         args={
        #             'har': 1,
        #             'html': 1,
        #         }
        #     )

    def parse_link(self, response):
        print("PARSED", response.real_url, response.url)
        print(response.css("title").extract())
        print(response.data["har"]["log"]["pages"])
        print(response.headers.get('Content-Type'))
