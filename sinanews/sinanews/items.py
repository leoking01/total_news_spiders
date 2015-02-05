# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from  scrapy import Item ,Field 


class SinanewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title=Field()
    link=Field()
    time_release=Field()
    response_news=Field()

    time_add=Field()
    hash=Field()

    append=Field()
    mark=Field()
    manufacturer=Field()
#    pass
    abstract=Field()
    mainbody=Field()

    encode =  Field()



