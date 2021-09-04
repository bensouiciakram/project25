# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TorrentsElasticItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    info_hash = scrapy.Field()
    