# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

import sys,os,hashlib

from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
from scrapy.utils.response import get_base_url
import crawl_body
from qqpro.items import QqproItem

import time
#sys.stdout=open('log.txt','w')

class sur_Spider(scrapy.Spider):
    name = "sur"
    allowed_domains = []
    start_urls = (
        'http://www.qq.com/',
    )

    #rules={
    #    Rule(LinkExtractor(allow=('.') ) ,callback='parse_surface_item'),
            
    #}

    #def parse_surface_item(self,response):
    def parse(self,response):
        print '=====parse_surface_item:=====response:',response
        sel_a=response.xpath('//div[contains(@id,"newsContent")]')
        sel_b=sel_a.xpath('.//ul')
        sel_c=sel_b.xpath('.//li')
        id=0        
        base_url = get_base_url(response)
        for site in sel_c:
            id+=1
            
            ##item: ...
            title=site.xpath('a/text()' ).extract()
            if len(title)!=0:
                link=site.xpath('a/@href' ).extract()
                response_news=['']

                item=QqproItem(title=title,link=link,response_news=response_news,\
                    manufacturer='surface')

                url_m= (str(link))[3:-2]
                #url_m= ''.join(link)
                url_new=urljoin(base_url,url_m )
                yield scrapy.Request(url_new, callback=self.parse_body,meta={'item':item})

                #print 'parse: item: ',item
                #yield item


        ##正文抓取
        #for site in response.xpath('//em[@class]'):
        #for site in sel_c:
        #    print 'body loop:'
        #    print 'response = ',response
        #    title=site.xpath('a/text()' ).extract()
        #    if len(title)!=0:
        #        link=site.xpath('a/@href' ).extract()
        #        url_m= (str(link))[3:-2]
        #        #url_m= ''.join(link)
        #        url_new=urljoin(base_url,url_m )
        #        yield scrapy.Request(url_new, callback=self.parse_body,meta={'item':item})
   
   
    ##正文抓取函数
    def parse_body(self,response):
        print 'done'
        print 'parse_body: create dir-file,write in...'
        print 'parse_body: response: ',response
        item=response.meta['item']
   
        #建立文件路径
        old_path='/data/news_data/qq_news/'
        t=time.localtime()
        t=time.strftime('%Y_%m_%d',t)
        new_path=os.path.join(old_path,t)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
    
    
        #建立文件名
        file=''
        hash=0
        title=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/h1/text()').extract()
        print 'parse_body: title: ',''.join(title).encode('utf-8')
        if len(title)!=0:
            ##title_a=''.join(title)
            title_a=''.join(title[0]).encode('utf-8')
            ##title_a=str( ( title[0] ) ).encode('utf-8')
            sha1obj = hashlib.sha1()
            sha1obj.update(title_a)
            hash = sha1obj.hexdigest()
            print 'hash: ',hash
            file=new_path+'/'+hash##hash 值作为文件名
            item['hash']=[hash]

            ##读取当前路径下文件列表、并判断
            res=os.listdir(new_path)
            print 'parse_body: type(res): ',type(res)
            print 'parse_body: res: ',res
            #print 'res:',str(res).encode('utf-8')
            pl=0
            for sh in res:
                if sh==hash:
                    pl=1
                    print '文件已经存在：hash:',hash
                    if os.path.getsize(new_path+'/'+''.join(sh) )<200:
                        pl=0
                        print '文件应存在:但内容过少，需要重写. hash: ',hash
            print 'pl:',pl

            ##开始写一个文本
            path='/data/news_data/'
            pl=crawl_body.file_check(path,hash)
            if pl==0:
                ##打开文件
                print '文件写入开始。hash: ',hash
                fp=open(file,'w')
        
                ##抓取、写入正文标题
                ##获取标题、取hash值
                title=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/h1/text()').extract()
                print 'title: ',''.join(title[0]).encode('utf-8')
                ##写入标题
                fp.write( 'title:\n' )
                #fp.write( str( title[0].encode('utf-8') ) )
                fp.write( ''.join(title[0]).encode('utf-8') ) 
                fp.write( '\n' )
        
                ##获取新闻发布时间、写入发布时间
                time_release_t=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/div[1]/div[1]/span[@class="article-time"]/text()  |  //*[@id="time_source"]/span/text()').extract()
                item['time_release']= [  ''.join(time_release_t).encode('utf-8') ]
                if len(time_release_t)==0:
                    item['time_release']=['']
                time_release= ''.join(time_release_t).encode('utf-8')
                print 'parse_body: time_release: ',time_release
                fp.write( 'time_release:\n' )
                fp.write( time_release )
                fp.write('\n')
        
                ##获取摘要、写入摘要 
                abstract=response.xpath('//*[@id=\'Cnt-Main-Article-QQ\']/p[1]/text()').extract()
                print 'parse_body: abstract: ',''.join(abstract).encode('utf-8')##abstract 是有可能为空的,故不能给定索引.
                item['abstract']=abstract
                fp.write( 'abstract:\n' )
                fp.write( ''.join(abstract ).encode('utf-8') )
                fp.write('\n')
        
                ##抓取正文
                bodys_a=response.xpath('//div[@id=\'Cnt-Main-Article-QQ\']')
                bodys_b=bodys_a.xpath('.//p')
                ##写入正文
                fp.write('main_body: \n')
                print 'main_body: '
                fp.write('\n')
                for bod in bodys_b:
                    main_body=bod.xpath('text()').extract()
                    if len(main_body)!=0:
                        print ''.join(main_body[0]).encode('utf-8')
                        ##写入正文各段
                        #fp.write( str( main_body[0].encode('utf-8') ) )
                        fp.write( ''.join( main_body[0]).encode('utf-8')  )
                        fp.write('\n')
    
                ##关闭文件
                fp.close()
                print 'finish.'
                return item
    
            else:
                print 'pl: ',pl
                print '由于文件已经存在.无操作。'
    
        else:
            item['time_release']=['']
            item['hash']=['']
            print '标题为空。不操作。'
        print '\n\n'
        #return item 
    
    
