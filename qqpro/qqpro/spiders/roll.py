# -*- coding: utf-8 -*-
##roll 
##滚动新闻没办法抓到ul

import scrapy
from qqpro.items import QqproItem
from scrapy import Selector

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

import sys
#sys.stdout=open('roll.txt','w')

class roll_Spider(CrawlSpider):
    name = "roll"
    #allowed_domains = ["news.qq.com"]
    allowed_domains = ['roll.news.qq.com']
    start_urls = (
        #'http://news.qq.com/',
        #'http://news.qq.com/china_index.shtml',
        #'http://news.qq.com/society_index.shtml',
        'http://roll.news.qq.com/',
    )

    rules={
        #Rule(LinkExtractor(allow=('.'), ) ,callback='parse_base_item'),
        #Rule(LinkExtractor(allow=('china_index.shtml',) ) ,callback='parse_china_item'),
        #Rule(LinkExtractor(allow=('society_index.shtml',) ) ,callback='parse_society_item'),
        Rule(LinkExtractor(allow=('.') ) ,callback='parse_roll_item'),
        #Rule(LinkExtractor(allow=('.htm',) ) ,callback='text_item'),
            
    }


    def parse_roll_item(self,response):
        print '=====parse_roll_item:=====response:',response
        #sel=Selector(response)
        #sel_a=response.xpath('//div[@class="main"]/div[@class="mainBody"]/div[@class="mainCon"]/div[@class="list c"]')
        sel_a=response.xpath('//*[@id=\'artContainer\']')
        #sel_a=response.xpath('/html/body/div[@id="iBody"]/div[@class="wrap c"]/div[@class="main"]/div[@class="mainBody"]/div[@class="mainCon"]/div[@id="artContainer"]/ul/li')
        #sel_m=sel_a.xpath('.//div[@id="artContainer"]/ul/li')
        #sel_a=sel
        sel_b=response.xpath('//ul')
        sel_c=sel_b.xpath('//li')
        print 'sel_a : ',sel_a
        print 'sel_b : ',sel_b
        print 'sel_c : ',sel_c
        #print 'sel_m : ',sel_m
        id=0        
        for site in sel_c:
            id+=1

            title=site.xpath('a/text()' ).extract()
            link=site.xpath('a/@href' ).extract()
            time_release=site.xpath('span[2]/text() ').extract()
            response_news=site.xpath('a/text() ').extract()
            #type_news=site.xpath('span[@class="t-tit"]/text()' ).extract()
            type_news=site.xpath('span[2]/text()' ).extract()

            item=QqproItem(title=title,link=link,time_release=time_release,type_news=type_news,response_news=response_news)

            print 'id : ',id
            print 'response :  ',response
            if not len(item['response_news'])==0:
                print 'response_news:',item['response_news'][0].encode('utf-8')
            else:
                print 'response_news','null'

            if not len(item['title'])==0:
                print 'title:',item['title'][0].encode('utf-8')
            else:
                print 'title:','null'
            yield QqproItem(title=title,link=link,time_release=time_release,type_news=type_news,response_news=response_news)


#    def parse(self,response):
#        print 'main?'
#        pass
str="""

.//*[@id='artContainer']/ul[1]/li[1]/a

.//*[@id='artContainer']/ul[1]/li[2]/a
.//*[@id='artContainer']/ul[1]/li[3]/a
.//*[@id='artContainer']/ul[1]/li[4]/a


.//*[@id='artContainer']/ul[1]/li[5]/a


.//*[@id='artContainer']/ul[2]/li[1]/a



.//*[@id='artContainer']/ul[2]/li[2]/a

.//*[@id='artContainer']/ul[1]/li[1]/span[2]


.//*[@id='artContainer']/ul[10]/li[1]/a
"""
