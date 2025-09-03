from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from src.spiders.statcan_spider import StatCanSpider


def fetch_raw_data(items_per_page: int | None = None) -> list[dict]:
    """
    Run StatCanSpider in blocking mode, collect items into a list.
    Supports KeyboardInterrupt.

    Parameters
    ----------
    items_per_page : int, optional
        Number of sources per page. Overrides default ITEMS_PER_PAGE.

    Returns
    -------
    list[dict]
        Scraped records from StatCan.
    """
    results: list[dict] = []

    class CollectorPipeline:
        def process_item(self, item, spider):
            results.append(dict(item))
            return item

    settings = {
        **get_project_settings(),
        'ITEM_PIPELINES': {CollectorPipeline: 100},
        'LOG_ENABLED': False,
    }

    runner = CrawlerRunner(settings=settings)

    spider_kwargs = {}
    if items_per_page:
        spider_kwargs['items_per_page'] = items_per_page

    deferred = runner.crawl(StatCanSpider, **spider_kwargs)
    deferred.addBoth(lambda _: reactor.stop())

    try:
        reactor.run()  # blocking, Ctrl+C works
    except KeyboardInterrupt:
        print('\nCrawl interrupted by user!')
        reactor.stop()

    return results
