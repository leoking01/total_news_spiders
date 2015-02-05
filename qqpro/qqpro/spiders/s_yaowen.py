# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url

from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath

import datetime,time
import sys
import os

from qqpro.items import QqproItem

import hashlib,os,sys

import crawl_body
#sys.stdout=open('out.txt','w')

class QqSpider(CrawlSpider):
    name = "s_yaowen"
    allowed_domains = ['news.qq.com']
    start_urls = (
        'http://news.qq.com/',
    )
    
    ###抓取范围：仅仅是 新闻中心_要闻
    ###          news.qq.com
    def parse(self,response):
        #print '=====parse:response:',response
        id=0
        base_url = get_base_url(response)


        ##目录列表抓取
        sel_b=response.xpath('//em[@class]')
        for site in sel_b:
            #print 'contents loop:'
            #print 'response= ',response
            id+=1
            
            ##item: title link time res type
            title=site.xpath('span/span/a/text() ' ).extract()
            if len(title)!=0:
                link=site.xpath('span/span/a/@href' ).extract()
                time_release=['']
                #response_news=site.xpath('div[@class="Q-tpWrap"]/p[@class]/text() ').extract()
                response_news=site.xpath('./../p[@class]/text() ').extract()
                #type_news=site.xpath('span/span/a/text() ' ).extract()
            
                ##item: hash
                #title_a=''.join(title[0]).encode('utf-8')
                ##title_a=str( ( title ) ).encode('utf-8')##
                #sha1obj = hashlib.sha1()
                #sha1obj.update(title_a)
                #hash = sha1obj.hexdigest()
                #hash=[hash]##hash 为列表类型
                ##print 'spider: hash: ',hash
            
                #item=QqproItem(title=title,link=link,time_release=time_release,\
                #        response_news=response_news,hash=hash,\
                #        manufacturer='s_yaowen')
                url_m= (str(link))[3:-2]
                url_new=urljoin(base_url,url_m )
                item=QqproItem(title=title,link=url_new,\
                        response_news=response_news,\
                        manufacturer='s_yaowen')
                yield scrapy.Request(url_new, callback=self.parse_body,meta={'item':item})

                #print 'in the end: item: ',item 
                #print '2222.\n\n'
                #yield item

            #else:
                #pass
                #print 'parse: 标题为空，无操作。'
   
    ##正文抓取函数
    def parse_body(self,response):
        #print 'parse_body: create dir-file,write in...'
        #print 'response: ',response
        item=response.meta['item']
   
        #建立文件路径
        old_path='/data/news_data/qq_news/'
        t=time.localtime()
        t=time.strftime('%Y_%m_%d',t)
        new_path=os.path.join(old_path,t)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
    
        #建立文件名
        #t=time.localtime()
        #tt=time.strftime('%Y_%m_%d_%X',t).replace(':','_')
        ##file=new_path+'/'+tt##建立完成##用时间作为文件名
        title=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/h1/text()').extract()
        file=''
        #if len(title)!=0:
        #    title_a=str( ( title[0] )[:30] ).encode('utf-8')##取长度为30
        #    title_b=title_a.replace(' ','_').replace(':','_').replace('：','_')
        #    file=new_path+'/'+title_b ##用标题作为文件名
        if len(title)!=0:
            title_a= ''.join(  title[0]  ).encode('utf-8')##
            sha1obj = hashlib.sha1()
            sha1obj.update(title_a)
            hash = sha1obj.hexdigest()
            file=new_path+'/'+hash##hash 值作为文件名
            item['hash']=[hash]


            ##读取当前文件列表
            #res=os.listdir(new_path)
            #pl=0##文件不存在
            #for sh in res:
            #    if sh==hash:
            #        pl=1##文件存在
            #        if os.path.getsize(new_path+'/'+sh)<30:
            #            pl=0##文件为空文件
            path='/data/news_data/'
            pl=crawl_body.file_check(path,hash)
            if pl==0:##文件不存在
                #print '文件不存在。开始创建并写入文件.'
                ##打开文件
                fp=open(file,'w')
        
                ##抓取、写入正文标题
                #title=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/h1/text()').extract()
                #if len(title)!=0:
                #print 'title: ',title[0].encode('utf-8')
    
                ##写入标题
                fp.write( 'title:\n' )
                fp.write( str( title[0].encode('utf-8') ) )
                fp.write( '\n' )
        
                ##获取新闻发布时间、写入发布时间
                ##.//*[@id='C-Main-Article-QQ']/div[1]/div[1]/div[1]/span[5]
                ##.//*[@id='C-Main-Article-QQ']/div[1]/div/div[1]/span[6]
                #time_release=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/div[1]/div[1]/span[@class="article-time"]/text()|\
                #       //*[@id=\'C-Main-Article-QQ\']/div[1]/div[1]/div[1]/span[@class="article-time"]/text()  \
                #       ').extract()
                time_release=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/div[1]/div[1]/span[@class="article-time"]/text()').extract()
                time_release= ''.join(time_release).encode('utf-8')
                #print 'parse_body: time_release: ',time_release
                item['time_release']=time_release
                #print 'parse_body: item[\'time_release\'] :',item['time_release']
                fp.write( 'time_release:\n' )
                fp.write( time_release )
                fp.write('\n')
        
                ##获取摘要、写入摘要 
                abstract=response.xpath('//*[@id=\'Cnt-Main-Article-QQ\']/p[1]/text()').extract()
                #print 'parse_body: abstract: ',''.join(abstract).encode('utf-8')##abstract 是有可能为空的,故不能给定索引.
                item['abstract']=abstract
                fp.write( 'abstract:\n' )
                fp.write( ''.join(abstract ).encode('utf-8') )
                fp.write('\n')
        
                ##抓取正文
                bodys_a=response.xpath('//div[@id=\'Cnt-Main-Article-QQ\']')
                bodys_b=bodys_a.xpath('.//p')
    
                ##写入正文
                fp.write('main_body: \n')
                fp.write('\n')
                for bod in bodys_b:
                    main_body=bod.xpath('text()').extract()
                    if len(main_body)!=0:
                        #print 'main_body: ',main_body[0].encode('utf-8')
                        ##写入正文各段
                        fp.write( str( main_body[0].encode('utf-8') ) )
                        fp.write('\n')
    
                ##关闭文件
                fp.close()
                return item 
            else:
                pass
                #print '文件已经存在。且不需要重新写入.'
        else:
            pass
            #print 'parse_body: 标题为空,无操作。\n\n'
    
    
    
