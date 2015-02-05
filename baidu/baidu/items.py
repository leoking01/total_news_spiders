# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from  scrapy import Item,Field


class BaiduItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    pass
    title=Field()
    link=Field()
    response_news=Field()
    encode = Field()

    hash=Field()
    time_release=Field()

    manufacturer=Field()
    tiem_add=Field()

    path=Field()
    mainbody = Field()

