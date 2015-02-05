# -*- coding: utf-8 -*-
import datetime

from sinanews.items import SinanewsItem  
from urlparse import urljoin
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector,Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

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

import time
from check import file_check

sys.stdout=open('log.txt','w')

class SinaSpider(scrapy.Spider):
    name = "sina"
    #allowed_domains = ["sina.com.cn"]
    allowed_domains = []
    start_urls = (
        ##只考虑国内新闻
        'http://news.sina.com.cn/china/',
    )


    def parse(self, response):
        sel_a=response.xpath('//div[contains(@id, \'subShowContent\')]')
        sel_c=sel_a.xpath('.//div')

        base_url = get_base_url(response)

        for site in sel_c:
            title=site.xpath('h2/a/text()').extract()

            ##爬取正文
            if len(title)!=0:
                link=site.xpath('h2/a/@href').extract()
                time_release=site.xpath('div/div[@class="time"]/text()').extract()
                response_news=['']

                url_m= (str(link))[3:-2]
                #url_m= ''.join(link)
                url_new=urljoin(base_url,url_m )
                print 'parse: url_new: ', url_new

                item =SinanewsItem(title=title,link=url_new,time_release=time_release,\
                    response_news=response_news,\
                    manufacturer=['sina_guonei'] )

                ##考虑到很多链接并不是基于url_base的，所以采用url_m. 因为url-m也是完整的。
                #yield scrapy.Request(url_new, callback=self.parse_body,meta={'item':item})
                yield scrapy.Request(url_m, callback=self.parse_body,meta={'item':item})

                print 'parse: item:',item
                #yield item 


   
   
    ##正文抓取函数
    def parse_body(self,response):
        print 'done'
        print 'parse_body: create dir-file,write in...'
        print 'parse_body: response: ',response
        item=response.meta['item']
   
        ##encode
        encode_0 = response.xpath('/html/head')
        encode_1 = encode_0.xpath('.//meta')
        encode_3 = ''
        for en in encode_1:
            encode_2 = en.xpath('@content').extract()
            ##encode_2 = str(encode_2)
            if len(encode_2)!=0:
                encode_2 = encode_2[0]
                if encode_2.find('charset') != -1:
                    encode_3 = encode_2.encode('utf-8')
        encode_3 = encode_3.strip('text').strip('/').strip('html').strip('; ').strip('charset=')
        print 'parse_body: head : encode_3 :',encode_3
        item['encode'] = encode_3

        #建立文件路径
        old_path='/data/news_data/sina_news/'
        t=time.localtime()
        t=time.strftime('%Y_%m_%d',t)
        new_path=os.path.join(old_path,t)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
    
        #建立文件名
        file=''
        hash=0
        title=response.xpath('.//*[@id=\'artibodyTitle\']/text()  ').extract()
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
            #sts=0
            #for sh in res:
            #    if sh==hash:
            #        sts=1
            #        print '文件已经存在：hash:',hash
            #        if os.path.getsize(new_path+'/'+''.join(sh) )<200:
            #            sts=0
            #            print '文件已经存在:但内容过少，需要重写. hash: ',hash
            #print 'sts: ',sts
            ##
            ##
            path='/data/news_data/'
            sts = file_check(path,hash)


            ##开始写一个文本
            sts = 0   ##无条件爬取
            ##pl=0  ####作为测试。强制要求所有数据重写。正式版中应注释掉。
            if sts==0:
                ##打开文件
                print '文件写入开始。hash: ',hash
                ##fp=open(file,'w')
        
                ##抓取、写入正文标题
                ##获取标题、取hash值
                #title=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/h1/text()').extract()
                print 'title: ',''.join(title[0]).encode('utf-8')
                ##写入标题
                #fp.write( 'title:\n' )
                #fp.write( str( title[0].encode('utf-8') ) )
                #fp.write( ''.join(title[0]).encode('utf-8') ) 
                #fp.write( '\n' )
        
                ##获取新闻发布时间、写入发布时间
                ##time_release_t=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/div[1]/div[1]/span[@class="article-time"]/text()  |  //*[@id="time_source"]/span/text()').extract()
                ##item['time_release']= [  ''.join(time_release_t).encode('utf-8') ]
                ##if len(time_release_t)==0:
                ##    item['time_release']=['']
                ##time_release= ''.join(time_release_t).encode('utf-8')
                ##print 'parse_body: time_release: ',time_release
                #3fp.write( 'time_release:\n' )
                ##fp.write( time_release )
                ##if len(item['time_release'] )!=0:
                ##    fp.write( ''.join(item['time_release'] ).encode('utf-8') )
                ##fp.write('\n')
        
                ##获取摘要、写入摘要 
                #abstract=response.xpath('//*[@id=\'Cnt-Main-Article-QQ\']/p[1]/text()').extract()
                #print 'parse_body: abstract: ',''.join(abstract).encode('utf-8')##abstract 是有可能为空的,故不能给定索引.
                #item['abstract']=abstract
                #fp.write( 'abstract:\n' )
                #fp.write( ''.join(abstract ).encode('utf-8') )
                #fp.write('\n')
        
                ##抓取正文
                bodys_a=response.xpath('//*[@id=\'artibody\']  ') 
                bodys_b=bodys_a.xpath('.//p')
                ##写入正文
                ##fp.write('main_body: \n')
                ##print 'main_body: '
                ##fp.write('\n')
                main_bodys = []
                for bod in bodys_b:
                    main_body = bod.xpath('text()').extract()
                    if len(main_body) !=  0:
                        print ''.join(main_body[0]).encode('utf-8')
                        ##写入正文各段
                        #fp.write( str( main_body[0].encode('utf-8') ) )
                        #fp.write( ''.join( main_body[0]).encode('utf-8')  )
                        #fp.write('\n')
                        main_bodys.append( ''.join( main_body[0] ) )
                item['mainbody'] = main_bodys
    
                ##关闭文件
                ##fp.close()
                print 'finish.'
                return item
    
            else:
                print 'sts: ',sts
                print '由于文件已经存在.无操作。'

    
        else:
            item['time_release']=['']
            item['hash']=['']
            print '标题为空。不操作。'
        print '\n\n'
        #return item 
    
    
