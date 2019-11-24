# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FishItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    date_ = scrapy.Field()
    md5 = scrapy.Field()
    create_time = scrapy.Field()


class FinanceNewsItem(scrapy.Item):

    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()

    source = scrapy.Field()
