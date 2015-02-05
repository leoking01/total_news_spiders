# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

import sys,os,hashlib

from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
from scrapy.utils.response import get_base_url

import scrapy
from scrapy.http import Request

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector,Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from baidu.items import BaiduItem
import scrapy

import datetime
import time

import crawl_body

sys.stdout=open('out.txt','w')

class BaiduguoneiSpider(scrapy.Spider):
    name = "baiduguonei"
    allowed_domains = []
    start_urls = (
        'http://guonei.news.baidu.com/',##百度 国内首页
        'http://shehui.news.baidu.com/n?cmd=4&class=socianews&pn=1',##百度 社会最新首页
        'http://news.baidu.com/n?cmd=4&class=shyf&pn=1',##百度社会与法
        'http://news.baidu.com/n?cmd=4&class=civilnews&pn=1&from=tab',##百度国内最新首页
    )


    def parse(self, response):
        sel=Selector(response)
        sel_0=sel.xpath('/html/body/div[@id="body"]')
        sel_1=sel_0.xpath('.//ul/li')
        base_url = get_base_url(response)
        no=0
        for site in sel_1:
            no+=1
            title=site.xpath('a/text()').extract()
            if ( len(title)!=0 and len( ''.join(title) )>4 ):
                link=site.xpath('a/@href').extract()
    
                url_m= (str(link))[3:-2]
                url_new=urljoin(base_url,url_m )
                item = BaiduItem(title=title,link=link,manufacturer='baiduguonei')

                yield scrapy.Request(url_new, callback=self.parse_body,meta={'item':item})



#######################################################################################


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
        old_path='/data/news_data/baidu_news/'
        t=time.localtime()
        t=time.strftime('%Y_%m_%d',t)
        new_path=os.path.join(old_path,t)
        item['path'] = new_path
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        ##item['path'] = ''.join( new_path )
            
    
        #建立文件名
        file=''
        hash=0
        bodys = response.xpath('//body')

        title = bodys.xpath('.//h1/text()  |  ../*[contains(@*,\'titl\')]').extract()
        ##time_release_t = bodys.xpath(' .//*[ contains(@*,\'time\') ]/text() ' ).extract()
        time_release_t = bodys.xpath(' .//*[ contains(@*,\'time\') ]/text() |  //*[@class=\'conText\']/div[@class="summaryNew"]/text() | //div[@class="left-time"]/div[@class="left-t"]/text()  | //*[@id=\'k_left\']/div[2]/div/p/span[2]/text()  |  //*[@id=\'C-Main-Article-QQ\']/div[1]/div[1]/div[1]/span[5]   |  /html/body/div[8]/div[1]/div[4]/text() | //*[@id=\'pubtime_baidu\']/text()   ').extract()
        ##title=response.xpath('//*[@class=\'conText\']/h1/text() | //div[@class="content"]/h1/text()  | //div[@class="main"]/h1/text()  | //*[@id=\'C-Main-Article-QQ\']/div[1]/h1   | /html/body/div[8]/div[1]/div[2]/text() | html/body/div[10]/div[1]/div[1]/text() ').extract()
        print 'parse_body: title: ',''.join(title).encode('utf-8')
        if ( len(title)!=0 and len( ''.join(title) ) >3 ):
            ##title_a=''.join(title)
            title_a=''.join(title[0]).encode('utf-8')
            ##title_a=str( ( title[0] ) ).encode('utf-8')
            sha1obj = hashlib.sha1()
            sha1obj.update(title_a)
            hash = sha1obj.hexdigest()
            print 'hash: ',hash
            file = new_path+'/'+hash##hash 值作为文件名
            item['hash'] = [hash]

            ##检查文件是否在已知路径中存在
            path='/data/news_data'
            pl = crawl_body.file_check(path,hash)
            ##pl=file_check(path,hash)
            ##开始写一个文本
            if pl==0:
                ##打开文件
                print '文件写入开始。hash: ',hash
                ##fp = open(file,'w')
        
                ##抓取、写入正文标题
                ##获取标题、取hash值
                ##print 'title: ',''.join(title[0]).encode('utf-8')
                ##写入标题
                ##fp.write( 'title:\n' )
                #fp.write( str( title[0].encode('utf-8') ) )
                ##fp.write( ''.join(title[0]).encode('utf-8') ) 
                ##fp.write( '\n' )
        
                ##获取新闻发布时间、写入发布时间
                ##time_release_t=response.xpath('//*[@class=\'conText\']/div[@class="summaryNew"]/text() | //div[@class="left-time"]/div[@class="left-t"]/text()  | //*[@id=\'k_left\']/div[2]/div/p/span[2]/text()  |  //*[@id=\'C-Main-Article-QQ\']/div[1]/div[1]/div[1]/span[5]   |  /html/body/div[8]/div[1]/div[4]/text() | //*[@id=\'pubtime_baidu\']/text()   ').extract()
                item['time_release']= [  ''.join(time_release_t).encode('utf-8') ]
                if len(time_release_t)==0:
                    item['time_release']=['']
                time_release= ''.join(time_release_t).encode('utf-8')
                print 'parse_body: time_release: ',time_release
                #fp.write( 'time_release:\n' )
                #fp.write( time_release )
                #fp.write('\n')

                ##response
                #fp.write( 'response:\n' )
                #fp.write( str(response)[5:] )
                #fp.write('\n')

        
                ##获取摘要、写入摘要 
                #abstract=response.xpath('//*[@id=\'Cnt-Main-Article-QQ\']/p[1]/text()').extract()
                #print 'parse_body: abstract: ',''.join(abstract).encode('utf-8')##abstract 是有可能为空的,故不能给定索引.
                #item['abstract']=abstract
                #fp.write( 'abstract:\n' )
                #fp.write( ''.join(abstract ).encode('utf-8') )
                #fp.write('\n')
        
                ##抓取正文
                ##bodys_a=response.xpath('//*[contains(@class,\'title\')]')
                bodys_b = bodys.xpath('.//p')
                ##print 'bodys_b : ', bodys_b
                ##bodys_c = bodys_a.xpath('.//p')
                ##写入正文
                ##fp.write('main_body: \n')
                main_bodys = []
                print 'main_body: '
                for bod in bodys_b:
                    print 'bod: ',bod
                    main_body = bod.xpath('text()').extract()
                    if len(main_body) != 0:
                        main_body = main_body[0]
                        if ( len(main_body)!=0 and len(''.join(main_body) ) >30 ) :
                            print ''.join(main_body).encode('utf-8')
                            ##写入正文各段
                            #fp.write( ''.join( main_body).encode('utf-8')  )
                            #fp.write('\n')
                            main_bodys.append(main_body)
                item['mainbody'] = main_bodys
    
                ##关闭文件
                ##fp.close()
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
    
    
##文件检查函数: 检查文件是否在某路径下存在.
##参数path: 路径
##    hash: 哈希值，即文件名
##返回值：0 -- 文件不存在
##        1 -- 文件已经存在
def file_check(path,hash):
    dirs_base=path
    dirs_main=os.listdir(dirs_base)
    state=0
    #print '******   main_directors list:  ******'
    #print dirs_base,' :'
    #print dirs_main

    for d in dirs_main:
        dir_0='/data/news_data/'+d
        #print '\n'
        #print '******   dir_0 = ',dir_0,'   ******'
        for dir_a in os.listdir(dir_0):
            dir_b=dir_0+'/'+dir_a
            #print 'The number of files in ', dir_b, ' is: ',len( os.listdir(dir_b) )
            for file in os.listdir(dir_b):
                if hash==file:
                    state=1
                    #print 'found: 文件 %s 存在于文件夹 %s 中.' %(hash,dir_b)
                    return state
                else:
                    state=0
    #print 'finish.'
    return state
    
    
