# -*- coding: utf-8 -*-
import scrapy
from qqpro.items import QqproItem
from scrapy import Selector

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

import datetime,time
import sys

from scrapy.utils.response import get_base_url
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath

import os,hashlib
import crawl_body

#sys.stdout=open('out.txt','w')
class QqSpider(CrawlSpider):
    name = "qq"
    allowed_domains = ['news.qq.com']
    start_urls = (
        'http://news.qq.com/',
    )

    rules=(
        ########一：新闻中心_腾讯网_要闻#######   http://news.qq.com/
        Rule(LinkExtractor(allow=('.', ) ) ,callback='parse_base_item', follow='true'),
        ########二：新闻中心_国内新闻#######   http://news.qq.com/china_index.shtml
        Rule(LinkExtractor(allow=('china_index.shtml',) ) ,callback='parse_china_item'),
        ########三：新闻中心_社会新闻#######   http://news.qq.com/society_index.shtml
        Rule(LinkExtractor(allow=('society_index.shtml',) ) ,callback='parse_society_item'),
        ##正文提取
        #Rule(LinkExtractor( allow=('.html' ,) ) , callback='parse_content_1' ),
    )
   
    #def parse(self,response):
    #    item=QqproItem()
    #    url_0='http://news.qq.com/'
    #    yield scrapy.Request(url_0, callback=self.parse_base_item,meta={'item':item})
    
    ######## 一：新闻中心_要闻 #######
    def parse_base_item(self,response):
        ###  (1)新闻中心_要闻
        print '=====parse_base_item:=====response:',response
        base_url = get_base_url(response)
        sel_a=response.xpath('//div[@id="news"]')
        sel_b=sel_a.xpath('.//div[@class="Q-tpWrap"]')
        id=0       
        ##爬取主页新闻标题列表
        for site in response.xpath('//em[@class]'):
            id+=1
            title=site.xpath('span/span/a/text() ' ).extract()
            link=site.xpath('span/span/a/@href' ).extract()
            response_news=site.xpath('../p[@class]/text() ').extract()

            
            ##show contents
            item=QqproItem(title=title,link=link,\
                    response_news=response_news,\
                    manufacturer='qq_center_yaowen')

            ##正文抓取
            print 'main body loop:'
            print 'response = ',response
            link=site.xpath('span/span/a/@href' ).extract()
            url_n= ''.join(link)
            url_new=urljoin(base_url,url_n )
            yield scrapy.Request(url_new, callback=self.parse_body_center_yaowen,meta={'item':item})

    ##新闻中心  要闻  正文
    def parse_body_center_yaowen(self,response):
        print 'parse_body_center_yaowen : done '
        print 'response: ',response
        print '####################### '
        item=response.meta('item')
        #文件路径
        old_path='/data/news_data/qq_news/'
        t=time.localtime()
        t=time.strftime('%Y-%m-%d',t)
        new_path=os.path.join(old_path,t)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        
        #新文件名
        t=time.localtime()
        tt=time.strftime('%Y_%m_%d_%X',t).replace(':','_')
        file=new_path+'/'+tt
        fp=open(file,'w')
        str='test word. \n'####test##ok.
        fp.write(str)
        fp.close()
        
            ##item: hash
            #title_a=''.join(title)
            #sha1obj = hashlib.sha1()
            #sha1obj.update(title_a)
            #hash = sha1obj.hexdigest()
            #print 'spider: hash: ',hash
        return item 


    ########二：新闻中心_国内#######
    def parse_china_item(self,response):
        print '=====parse_china_item:=====response:',response
        sel_a=response.xpath('.//div[@id="news"]')
        sel_b=sel_a.xpath('.//div[@class="Q-tpWrap"]')
        id=0        
        for site in sel_b:
            id+=1
            title=site.xpath('em[@class]/a/text() ' ).extract()
            link=site.xpath('em[@class]/a/@href' ).extract()
            #link="http://news.qq.com/"+str(link)
            #print "=============link:       ",link
            time_release=site.xpath('em[@class]/a/@href ').extract()
            response_news=site.xpath('p[@class]/text() ').extract()
            type_news=site.xpath('em[@class]/a/text() ' ).extract()

            ##item: hash
            title_a=''.join(title)
            sha1obj = hashlib.sha1()
            sha1obj.update(title_a)
            hash = sha1obj.hexdigest()
            print 'spider: hash: ',hash

            item=QqproItem(title=title,link=link,time_release=time_release,response_news=response_news,type_news=type_news,hash=hash,manufacturer='qq_center_china')


            print 'id : ',id
            print 'response :  ',response

            if not len(item['response_news'])==0:
                print 'response_news:',item['response_news'][0].encode('utf-8')
            else:
                print 'response_news:','response_news'

            if not len(item['title'])==0:
                print 'title:',item['title'][0].encode('utf-8')
            else:
                print 'title:','null'
            yield item
            ##yield QqproItem(title=title,link=link,time_release=time_release,response_news=response_news)

    



    ########三：新闻中心_社会#######
    def parse_society_item(self,response):
        print '=====parse_society_item:=====response:',response
        sel_a=response.xpath('.//div[@id="news"]')
        sel_b=sel_a.xpath('.//div[@class="Q-tpWrap"]')
        id=0        
        for site in sel_b:
            id+=1
            title=site.xpath('em[@class]/a/text()' ).extract()
            link=site.xpath('em[@class]/a/@href' ).extract()
            time_release=site.xpath('em[@class]/a/@href ').extract()
            response_news=site.xpath('p[@class]/text() ').extract()
            type_news=site.xpath('em[@class]/a/text()' ).extract()

            ##item: hash
            title_a=''.join(title)
            sha1obj = hashlib.sha1()
            sha1obj.update(title_a)
            hash = sha1obj.hexdigest()
            print 'spider: hash: ',hash

            item=QqproItem(title=title,link=link,time_release=time_release,response_news=response_news,type_news=type_news,hash=hash,manufacturer='qq_center_china')


            print 'id : ',id
            print 'response :  ',response

            if not len(item['response_news'])==0:
                print 'response_news:',item['response_news'][0].encode('utf-8')
            else:
                print 'response_news:','response_news'

            if not len(item['title'])==0:
                print 'title:',item['title'][0].encode('utf-8')
            else:
                print 'title:','null'

            yield item
            ##yield QqproItem(title=title,link=link,time_release=time_release,response_news=response_news)


#############################################################################
#############################################################################
#############################################################################

        ########四：滚动新闻：另做。以下不工作。#######
    def parse_roll_item(self,response):
        print '=====parse_roll_item:=====response:',response
        sel_a=response.xpath('//div[@class="main"]/div[@class="mainCon"]/div[@class="list c"]')
        sel_b=sel_a.xpath('.//ul')
        sel_b=sel_a.xpath('.//li')
        id=0        
        for site in sel_b:
            id+=1
            title=site.xpath('a/text()' ).extract()
            link=site.xpath('a/@href' ).extract()
            time_release=site.xpath('a/@href ').extract()
            type_news=site.xpath('span[@class="t-tit"]/text()' ).extract()
            #response_news=site.xpath('p[@class]/text() ').extract()

            item=QqproItem(title=title,link=link,time_release=time_release,type_news=type_news)
            print 'id : ',id
            print 'response :  ',response
            print 'response_news:',item['response_news'][0].encode('utf-8')
            if not len(item['title'])==0:
                print 'title:',item['title'][0].encode('utf-8')
            else:
                print 'title:','null'
            yield QqproItem(title=title,link=link,time_release=time_release,type_news=type_news)


#    def parse(self,response):
#        print 'oooooooooooooo','   parse '
#        pass


###################################################################################################################

######   ********************************************************************************************8

#    def parse(self,response):
#        print 'main?'
#        pass
        #parse_base_item(self,response)
#        item=QqproItem()
#        return item



#    def parse(self, response):
#        sel=response.xpath('//a')
#        id=0
#        for h3 in sel.xpath('text()'):
#            id+=1
#            title=h3.extract()
#            link=h3.xpath('../@href').extract()
#            response_news=h3.xpath('../../p/text()').extract()
#            if not len(title)==0:
#                item=QqproItem(title=title,link=link,time_release=link,response_news=response_news)
#                print 'id: ',id
#                arg=item['title']
#                print '%s'% arg
#                yield QqproItem(title=title,link=link,\
#                    time_release=link,response_news=response_news)
        

#        for url in sel.xpath('@href').extract():
#            print 'second yield called.'
#            yield scrapy.Request(url, callback=self.parse)
        
#        pass
#        sel=Selector(response)
#        sel_0=sel.xpath('/html/body/div[@class="layout Q-g16b-b"]/div[@class="chief"]/div[@id="news"]/div[@class="bd"]/div[@id="mainTabPanel0"]/div[@role="tabpane1"]')
#        sel_1=sel_0.xpath('//div[@class="Q-tpList"]/div[@class="Q-tpWrap"]')
        ##要闻
#        sel_a=sel.xpath('//div[@id="news"]')
#        sel_b=sel_a.xpath('//div[@class="Q-tpWrap"]')
#        print 'type_news(sel_b): ',type_news(sel_b)
        ##国内新闻第一页
        ##社会新闻第一页

#        for site in sel_b:

            #title=site.xpath('em[@class]/span/span/a/text() ' or ' em[@class]/a/text()').extract()
            #link=site.xpath('em[@class]/span/span/a/@href' or ' em[@class]/a/@href').extract()
            #time_release=site.xpath('em[@class]/span/span/a/@href 'or ' em[@class]/a/@href').extract()
            #response_news=site.xpath('p[@class]/text() 'or ' em[@class]/p[@class]/text()').extract()
            
#            item=QqproItem(title=title,link=link,\
#                time_release=time_release,response_news=response_news)
            #print item
#            if not len(item['title'])==0:
#                arg=item['title'][0]
#                print '%s' % arg
                #print 'title: ',item['title'][0].encode('utf-8')
#            if not len(item['title'])==0:
#                yield QqproItem(title=title,link=link,\
#                    time_release=time_release,response_news=response_news)


