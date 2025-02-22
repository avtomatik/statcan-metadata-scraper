import re

import scrapy

from statcan_web_scraper.settings import (ALLOWED_DOMAINS, SPIDER_NAME,
                                          START_URLS)


class BaseSpider(scrapy.Spider):
    name = SPIDER_NAME
    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URLS

    def get_number_of_sources(self, response):
        summary_string = response.css('summary').get()
        pattern = r'\((?P<number_string>\d{1,3}(?:,\d{3})*)\)'
        match = re.search(pattern, summary_string)
        if match:
            return int(match.group('number_string').replace(',', ''))
        return 0

    def parse(self, response):
        # =====================================================================
        # TODO: Replace `print`s with Logging, Level Debug
        # =====================================================================
        number_of_sources = self.get_number_of_sources(response)
        page_size = 100
        print(f'Number of Sources: {number_of_sources}')
        for _ in range(1 + number_of_sources // page_size):
            print(
                f'Parsing Page {1 + _:3} Out of {1 + number_of_sources // page_size}'  # noqa: E501
            )
