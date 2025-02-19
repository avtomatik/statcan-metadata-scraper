import scrapy

from statcan_web_scraper.settings import (ALLOWED_DOMAINS, SPIDER_NAME,
                                          START_URLS)


class ExampleSpider(scrapy.Spider):
    name = SPIDER_NAME
    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URLS

    def parse(self, response):
        pass
