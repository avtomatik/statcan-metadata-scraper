import scrapy

from src.core.config import ITEMS_PER_PAGE, PAGE_URL


class StatCanSpider(scrapy.Spider):
    name = 'statcan'
    allowed_domains = ['www150.statcan.gc.ca']

    items_per_page: int = ITEMS_PER_PAGE

    custom_settings = {
        'LOG_ENABLED': False,  # disable logging if desired
        # Add more per-spider settings if needed
        # 'DOWNLOAD_DELAY': 0.5,
        # 'CONCURRENT_REQUESTS': 8,
    }

    def __init__(self, items_per_page=None, *args, **kwargs):
        """
        Allow overriding items_per_page via spider argument.
        Example: scrapy crawl statcan -a items_per_page=50
        """
        super().__init__(*args, **kwargs)
        if items_per_page:
            self.items_per_page = int(items_per_page)

    def start_requests(self):
        yield scrapy.Request(PAGE_URL, callback=self.parse_total_sources)

    def parse_total_sources(self, response):
        summary_text = response.css('summary::text').get()
        total_sources = int(
            summary_text.strip().split('(')[1].split(')')[0].replace(',', '')
        )

        total_pages = 1 + total_sources // self.items_per_page

        url_template = PAGE_URL  # already has count/pagination placeholders

        for page_idx in range(total_pages):
            yield scrapy.Request(
                url_template.format(self.items_per_page, page_idx),
                callback=self.parse_page,
            )

    def parse_page(self, response):
        items = response.css('details#all li.ndm-item')

        for item in items:
            yield {
                'title': item.css('.ndm-result-title::text').get(default='None'),
                'product_id': item.css('.ndm-result-productid::text').get(),
                'former_id': item.css('.ndm-result-formerid::text').get(default=''),
                'geo': item.css('.ndm-result-geo::text').get(default=''),
                'frequency': item.css('.ndm-result-freq::text').get(default=''),
                'description': item.css('.ndm-result-description::text').get(default=''),
                'release_date': item.css('.ndm-result-date::text').get(),
                'type': item.css('.ndm-result-productid::text').get().split(':')[0],
                'ref': item.css('a::attr(href)').get(),
            }
