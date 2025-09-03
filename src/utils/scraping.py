from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.spiders.statcan_spider import StatCanSpider


def fetch_raw_data() -> list[dict]:
    """
    Run the Scrapy spider programmatically and return collected records.

    Returns
    -------
    list[dict]
        List of raw data records scraped from StatCan.
    """
    results: list[dict] = []

    class CollectorPipeline:
        def process_item(self, item, spider):
            results.append(dict(item))
            return item

    process = CrawlerProcess(
        settings={
            **get_project_settings(),
            'ITEM_PIPELINES': {CollectorPipeline: 100},
            'LOG_ENABLED': False,
        }
    )

    process.crawl(StatCanSpider)
    process.start()

    return results
