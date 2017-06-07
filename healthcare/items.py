# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CWItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    import_date = scrapy.Field()
    sku = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    saved = scrapy.Field()
    url = scrapy.Field()
