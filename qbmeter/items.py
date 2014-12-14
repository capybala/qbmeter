# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Store(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    timestamp = scrapy.Field()


class Availability(scrapy.Item):
    store_id = scrapy.Field()
    signal = scrapy.Field()
    html = scrapy.Field()
    num_available = scrapy.Field()
    num_waiting = scrapy.Field()
    timestamp = scrapy.Field()
