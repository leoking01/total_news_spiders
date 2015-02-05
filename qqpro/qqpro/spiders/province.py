# -*- coding: utf-8 -*-

import scrapy
from qqpro.items import QqproItem
from scrapy import Selector

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
from scrapy.utils.response import get_base_url
import sys,hashlib,os

import crawl_body

import time

sys.stdout=open('log.txt','w')

class roll_Spider(CrawlSpider):
    name = "pro"
    allowed_domains = []
    start_urls = (
        'http://gd.qq.com/news/',    #大粤网
        'http://hb.qq.com/news/',    #大楚网
        #'http://hn.qq.com/',    #大湘网   不适合 ul/li/div/div 形式
        #'http://henan.qq.com/', #大豫网
        #'http://hb.jjj.qq.com/', #大燕网  也不适合啊
        #'cq.qq.com/',           #大渝网
        #http://cq.qq.com/CQxinwen/society/socnews.htm  ##大渝网资讯网
    )

    #rules={
        #Rule
    #    Rule(LinkExtractor(allow=('news/','CQxinwen/society/socnews.htm') ) ,callback='parse_pro_item'),
        #Rule(LinkExtractor(allow=('gd.qq.com/news/') ) ,callback='parse_pro_item'),
            
    #}

    #def parse_pro_item(self,response):
    def parse(self,response):
        print '=====parse_pro_item:=====response:',response
        #a:
        ########         /ul/li/div/div            ########
        #b:
        ########         /ul/li                    ########
        base_url = get_base_url(response)
        sel_b=response.xpath('//ul')
        sel_c=sel_b.xpath('.//li')
        sel_d=sel_c.xpath('.//div')
        sel_e=sel_d.xpath('.//div')
        id=0        
        for site in sel_e:
            id+=1
            #a:
#############################楚################粤########################
            title=site.xpath('h3/a/text()   |a/text()' ).extract()
            print 'title: ',title
            if len(title)!=0:
                link=site.xpath('h3/a/@href |a/@href' ).extract()
                #time_release=site.xpath('   ./../div[@class="pubTime"]/text()').extract()
                response_news=site.xpath('p/text() | ./../p/text() ').extract()
                #type_news=['']

                ##item: hash
                title_a= ''.join(title[0]).encode('utf-8')###严格的格式 
                sha1obj = hashlib.sha1()
                sha1obj.update(title_a)
                hash = sha1obj.hexdigest()
                hash=[hash]##item各项采用列表类型
                print 'spider: hash: ',hash
                #b:
#############################楚############################粤#######################湘、豫########
                #title=site.xpath('div/div[2]/h3/a/text()       |div[2]/div[1]/a/text() |a/text()').extract()
                #link=site.xpath('div/div[2]/h3/a/@href         |div[2]/div[1]/a/@href  |a/@href').extract()
                #time_release=site.xpath('div/div[2]/h3/a/@href |div[2]/div[1]/a/@href  |a/@href').extract()
                #response_news=site.xpath('div/p/text()         |div[2]/p/text()        |../p/text()').extract()
                #type_news=site.xpath('div/div[2]/h3/a/text()   |div[2]/div[1]/a/text() |a/text()').extract()

                url_m= ''.join(link)
                url_new=urljoin(base_url,url_m )

                item=QqproItem(title=title,\
                        link=url_new,\
                    response_news=response_news,\
                    manufacturer='province')

                #yield item

                yield scrapy.Request(url_new, callback=self.parse_body,meta={'item':item})
   
            else:
                print 'parse: 标题为空。不操作.\n\n'
   
   
###################################################3
   
    ##正文抓取函数
    def parse_body(self,response):
        print 'done'
        print 'parse_body: create dir-file,write in...'
        print 'parse_body: response: ',response
        #sel_a=response.xpath('//div[contains(@id,"newsContent")]')
        #sel_b=sel_a.xpath('.//ul')
        #sel_c=sel_b.xpath('.//li')
        item = response.meta['item']
   
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
        old_path='/data/news_data/qq_news/'
        t=time.localtime()
        t=time.strftime('%Y_%m_%d',t)
        new_path=os.path.join(old_path,t)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        item['path'] = new_path 
    
        #建立文件名
        file=''
        hash=0
        #items=[]
        title=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/h1/text()').extract()
        print 'parse_body: title: ',''.join(title).encode('utf-8')
        if len(title)!=0:
            title_a=''.join(title[0]).encode('utf-8')
            ##title_a=str( ( title[0] ) ).encode('utf-8')
            sha1obj = hashlib.sha1()
            sha1obj.update(title_a)
            hash = sha1obj.hexdigest()
            print 'hash: ',hash
            file=new_path+'/'+hash##hash 值作为文件名
            item['hash']=[hash]

            ##读取当前路径下文件列表、并判断
            #res=os.listdir(new_path)
            #print 'parse_body: type(res): ',type(res)
            #print 'parse_body: res: ',res
            #pl=0
            #for sh in res:
            #    if sh==hash:
            #        pl=1
            #        print '文件已经存在：hash:',hash
            #        if os.path.getsize(new_path+'/'+''.join(sh) )<200:
            #            pl=0
            #            print '文件应存在:但内容过少，需要重写. hash: ',hash
            #print 'pl:',pl
            #
            path='/data/news_data/'
            pl=crawl_body.file_check(path,hash)
            pl = 0  ##无条件爬取
            ##开始写一个文本
            if pl==0:
                ##打开文件
                print '文件写入开始。hash: ',hash
                #fp=open(file,'w')
        
                ##抓取、写入正文标题
                ##获取标题、取hash值
                title=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/h1/text()').extract()
                print 'title: ',''.join(title[0]).encode('utf-8')
                ##写入标题
                #fp.write( 'title:\n' )
                #fp.write( str( title[0].encode('utf-8') ) )
                #fp.write( ''.join(title[0]).encode('utf-8') ) 
                #fp.write( '\n' )
        
                ##获取新闻发布时间、写入发布时间
                time_release=response.xpath('//*[@id=\'C-Main-Article-QQ\']/div[1]/div[1]/div[1]/span[@class="article-time"]/text()').extract()
                time_release= ''.join(time_release).encode('utf-8')
                print 'parse_body: time_release: ',time_release
                item['time_release']=time_release
                #fp.write( 'time_release:\n' )
                #fp.write( time_release )
                #fp.write('\n')
        
                ##获取摘要、写入摘要 
                abstract=response.xpath('//*[@id=\'Cnt-Main-Article-QQ\']/p[1]/text()').extract()
                print 'parse_body: abstract: ',''.join(abstract).encode('utf-8')##abstract 是有可能为空的,故不能给定索引.
                item['abstract']=abstract
                #fp.write( 'abstract:\n' )
                #fp.write( ''.join(abstract ).encode('utf-8') )
                #fp.write('\n')
        
                ##抓取正文
                bodys_a=response.xpath('//div[@id=\'Cnt-Main-Article-QQ\']')
                bodys_b=bodys_a.xpath('.//p')
                ##写入正文
                #fp.write('main_body: \n')
                print 'main_body: '
                #fp.write('\n')
                bodys=[]
                for bod in bodys_b:
                    main_body=bod.xpath('text()').extract()
                    if len(main_body)!=0:
                        print ''.join(main_body[0]).encode('utf-8')
                        ##写入正文各段
                        #fp.write( str( main_body[0].encode('utf-8') ) )
                        #fp.write( ''.join( main_body[0]).encode('utf-8')  )
                        #fp.write('\n')
                        bodys.append( ''.join(main_body[0]) ) 
                item['mainbody'] = bodys
                #fp.write('finish.\n')
    
                    ##关闭文件
                ##fp.close()
                print 'finish.'
                item['mainbody']=bodys
                print 'intheend: item = ',item
        #        items.append(item)
                return item
    
            else:
                print 'pl: ',pl
                print '由于文件已经存在.无操作。'
    
        else:
            print 'parse_body: 标题为空。不操作。'
        print '\n\n\n'
#        return item
    
    
    
        


str="""
= = =  = = = = == = = = == = = = == = = = == = = == = = == = = == = = =
a:             大楚网 大粤网              
ul/li/div/div  h3/a/   a/
= = =  = = = = == = = = == = = = == = = = == = = == = = == = = == = = =


= = =  = = = = == = = = == = = = == = = = == = = == = = == = = == = = =
b:   ul/li/
大粤网      大楚网       大湘网 大豫网 大渝网(资讯网) 大燕网 
div/div/a/  div/div/h3/a a/     a/     span/a         div/h2/a
= = =  = = = = == = = = == = = = == = = = == = = == = = == = = == = = =


#############################################################
大粤网
html/body/div[4]/div[3]/div[1]/div[2]/div[1]/h3/a
头条
html/body/div[4]/div[7]/div[1]/div/div[2]/ul/li[1]/div[2]/div[1]/a
html/body/div[4]/div[7]/div[1]/div/div[2]/ul/li[4]/div[2]/div[1]/a
不能要这个
html/body/div[4]/div[7]/div[1]/div/div[1]/div/a[2]



#############################################################
大楚网
html/body/div[18]/div[1]/ul[1]/li[1]/div/div[2]/h3/a
html/body/div[18]/div[1]/ul[1]/li[1]/div/div[2]/h3/a
html/body/div[18]/div[1]/ul[1]/li[3]/div/div[2]/h3/a
.//*[@id='listimgzxb']/li[1]/div/h4/a
.//*[@id='listimgzxb']/li[2]/div/div[2]/h3/a
.//*[@id='listimgzxb']/li[3]/div/div[2]/h3/a
.//*[@id='listimgzxb']/li[4]/div/div[2]/h3/a
.//*[@id='listimgzxb']/li[8]/div/div[2]/h3/a  
==.//*[@id='listimgzxb']/li[8]/div/div[2]/h3/a/text() 
==/html/body/div[18]/div[1]/ul[2]/li[8]/div/div[2]/h3/a



#############################################################
大湘网
html/body/div[5]/div/div[1]/div/div[2]/div[2]/div[1]/h2/a
html/body/div[5]/div/div[1]/div/div[2]/div[2]/div[1]/div/ul/li[1]/a
html/body/div[5]/div/div[1]/div/div[2]/div[2]/div[2]/div/ul/li[4]/a

html/body/div[5]/div/div[5]/div/div[1]/div/div[1]/div/ul/li[1]/a
html/body/div[5]/div/div[5]/div/div[1]/div/div[2]/div/ul/li[1]/a
html/body/div[5]/div/div[5]/div/div[1]/div/div[3]/div/ul/li[2]/a
html/body/div[5]/div/div[5]/div/div[1]/div/div[4]/div/ul/li[4]/a



#############################################################
大豫网
html/body/div[3]/div[6]/div[2]/div[1]/h4/a
html/body/div[3]/div[6]/div[2]/div[2]/h4/a

html/body/div[3]/div[6]/div[2]/div[4]/div[1]/ul/li[1]/a
html/body/div[3]/div[6]/div[2]/div[4]/div[1]/ul/li[5]/a

html/body/div[3]/div[6]/div[2]/div[4]/div[2]/ul/li[1]/a
html/body/div[3]/div[6]/div[2]/div[4]/div[3]/ul/li[1]/a
html/body/div[3]/div[6]/div[2]/div[4]/div[4]/ul/li[1]/a



#############################################################
大渝网
http://cq.qq.com/news/
html/body/div[16]/div[2]/div[3]/h2/a
html/body/div[16]/div[2]/div[4]/h3/a
html/body/div[16]/div[2]/div[5]/div[2]/div[2]/div[2]/h1/a
html/body/div[16]/div[2]/div[5]/div[2]/div[9]/div[2]/h1/a
html/body/div[16]/div[2]/div[5]/div[2]/div[14]/div[2]/h1/a
html/body/div[16]/div[2]/div[5]/div[2]/div[16]/div[2]/h1/a

大渝网资讯
http://cq.qq.com/CQxinwen/society/socnews.htm
/html/body/div[4]/div/div[1]/div/div[2]/ul[3]/li[1]/span[1]/a
/html/body/div[4]/div/div[1]/div/div[2]/ul[3]/li[3]/span[1]/a



#############################################################
大燕网
html/body/div[4]/div[2]/div[2]/div[2]/ul/li[1]/div[1]/h2/a

html/body/div[4]/div[2]/div[2]/div[4]/ul/li[1]/div[1]/h2/a
html/body/div[4]/div[3]/div[2]/div[2]/ul/li[1]/div[1]/h2/a
html/body/div[4]/div[3]/div[2]/div[2]/ul/li[7]/div[1]/h2/a




"""








