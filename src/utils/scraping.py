import asyncio

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from twisted.internet import reactor

from src.spiders.statcan_spider import StatCanSpider


def fetch_raw_data() -> list[dict]:
    """
    Run the Scrapy spider programmatically and return collected records.
    """
    results: list[dict] = []

    def _item_collected(item, response, spider):
        results.append(dict(item))

    dispatcher.connect(_item_collected, signal=signals.item_passed)
    runner = CrawlerRunner()

    async def crawl():
        await runner.crawl(StatCanSpider)

    # Run Scrapy inside Twisted's reactor
    try:
        asyncio.get_event_loop().run_until_complete(crawl())
    except RuntimeError:
        # Fallback for environments where event loop is already running
        reactor.callWhenRunning(crawl)
        reactor.run()

    return results
