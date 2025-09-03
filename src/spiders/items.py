import scrapy


class StatCanItem(scrapy.Item):
    title = scrapy.Field()
    product_id = scrapy.Field()
    former_id = scrapy.Field()
    geo = scrapy.Field()
    frequency = scrapy.Field()
    description = scrapy.Field()
    release_date = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
