import scrapy

from src.core.config import PAGE_URL


class StatCanSpider(scrapy.Spider):
    name = 'statcan'

    def start_requests(self):
        yield scrapy.Request(PAGE_URL)

    def parse(self, response):
        # Extract total pages
        total_sources = int(response.css('summary::text').re_first(
            r'\(([\d,]+)\)').replace(',', '')
        )
        sources_per_page = 100
        total_pages = 1 + total_sources // sources_per_page

        for page_idx in range(total_pages):
            url = f'https://www150.statcan.gc.ca/n1/en/type/data?count={sources_per_page}&p={page_idx}-All#all'
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        items = response.css('details#all li.ndm-item')

        for item in items:
            yield {
                'title': item.css('.ndm-result-title::text').get(),
                'product_id': item.css('.ndm-result-productid::text').get(),
                'former_id': item.css('.ndm-result-formerid::text').get(default=''),
                'geo': item.css('.ndm-result-geo::text').get(default=''),
                'frequency': item.css('.ndm-result-freq::text').get(default=''),
                'description': item.css('.ndm-result-description::text').get(default=''),
                'release_date': item.css('.ndm-result-date::text').get(),
                'type': item.css('.ndm-result-productid::text').get().split(':')[0],
                'ref': item.css('a::attr(href)').get(),
            }
