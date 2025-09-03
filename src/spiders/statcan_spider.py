import scrapy
from scrapy.http import Request, Response

from src.spiders.items import StatCanItem
from src.spiders.settings import ITEMS_PER_PAGE, PAGE_URL


class StatCanSpider(scrapy.Spider):
    name = 'statcan'
    allowed_domains = ['www150.statcan.gc.ca']

    items_per_page: int = ITEMS_PER_PAGE

    custom_settings = {
        'LOG_ENABLED': False,  # disable logging if desired
        # 'DOWNLOAD_DELAY': 0.5,
        # 'CONCURRENT_REQUESTS': 8,
    }

    def __init__(
        self,
        items_per_page: int | None = None,
        *args,
        **kwargs
    ) -> None:
        """Allow overriding items_per_page via spider argument.
        Example: scrapy crawl statcan -a items_per_page=50
        """
        super().__init__(*args, **kwargs)
        if items_per_page:
            self.items_per_page = int(items_per_page)

    def start_requests(self):
        """Kick off crawl with the summary page to calculate total pages."""
        yield Request(PAGE_URL, callback=self.parse_total_sources)

    def parse_total_sources(self, response: Response):
        """Parse total number of sources from summary text, then paginate."""
        summary_text = response.css('summary::text').get()
        if not summary_text:
            self.logger.warning('No summary text found, skipping pagination.')
            return

        total_sources = int(
            summary_text.strip().split('(')[1].split(')')[0].replace(',', '')
        )
        total_pages = 1 + total_sources // self.items_per_page

        for page_idx in range(total_pages):
            yield Request(
                PAGE_URL.format(self.items_per_page, page_idx),
                callback=self.parse_page,
                cb_kwargs={'page_idx': page_idx},
            )

    def parse_page(self, response: Response, page_idx: int):
        """Extract all items from a paginated result page."""
        for item_sel in response.css('details#all li.ndm-item'):
            yield self.parse_item(item_sel)

    def parse_item(self, selector) -> StatCanItem:
        """Extract fields from a single result row into an Item."""
        product_id = selector.css('.ndm-result-productid::text').get()

        return StatCanItem(
            title=selector.css('.ndm-result-title::text').get(default=''),
            product_id=product_id,
            former_id=selector.css(
                '.ndm-result-formerid::text'
            ).get(default=''),
            geo=selector.css('.ndm-result-geo::text').get(default=''),
            frequency=selector.css('.ndm-result-freq::text').get(default=''),
            description=selector.css(
                '.ndm-result-description::text'
            ).get(default=''),
            release_date=selector.css('.ndm-result-date::text').get(),
            type=product_id.split(':')[0] if product_id else '',
            url=selector.css('a::attr(href)').get(),
        )
