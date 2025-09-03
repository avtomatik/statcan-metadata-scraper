import scrapy

from src.core.config import PAGE_URL


class StatCanSpider(scrapy.Spider):
    name = 'statcan'
    allowed_domains = ['www150.statcan.gc.ca']

    def start_requests(self):
        yield scrapy.Request(PAGE_URL, callback=self.parse_total_sources)

    def parse_total_sources(self, response):
        # Extract number inside parentheses, e.g. "(12,345)"
        summary_text = response.css('summary::text').get()
        total_sources = int(summary_text.strip().split(
            '(')[1].split(')')[0].replace(',', ''))

        sources_per_page = 100
        total_pages = 1 + total_sources // sources_per_page

        url_template = 'https://www150.statcan.gc.ca/n1/en/type/data?count={}&p={}-All#all'

        for page_idx in range(total_pages):
            yield scrapy.Request(
                url_template.format(sources_per_page, page_idx),
                callback=self.parse_page,
            )

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
