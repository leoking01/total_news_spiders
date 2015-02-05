# -*- coding: utf-8 -*-
"""
采用多条件判断的方式提取新闻标题和正文。
标题和链接：
1，链接长度频度最高。或者比较高。(链接长度统计----链接--标题搜集)

正文：
2. 正文字数不低于100字。(正文字数统计----正文-标题爬取)

其他：
3. 链接的层次只能是一层。(链接层数控制: 1)
4. 
"""
import sys,os,hashlib
import time

from twisted.enterprise import adbapi
import MySQLdb.cursors
import MySQLdb

import scrapy
from scrapy import Selector,signals,log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.xlib.pydispatch import dispatcher
from scrapy.utils.response import get_base_url

from urlparse import urljoin,urlparse,urlunparse
from posixpath import normpath

from chinanewspro.items import ChinanewsproItem

from file_check_function  import file_check
import file_check_function
import urls

from chinanews_functions import  list_2_dict,bianli,dict_max,dict_min,dict_modif,evaluation,dir_creat,list_evaluation,item_check

sys.path.append('/home/luokun/work/svn_103_scrapy_projects/common_functions')
from functions import  s_any_2_encoding, s_any_2_utf8

  
reload( sys )
sys.setdefaultencoding( 'utf8'  )
sys.stdout = open('log_scrapy_spider.txt','w')

import chardet

class ChinanewsSpider(scrapy.Spider):
    name = "all_news"
    allowed_domains = []
    start_urls = urls.all_urls 
   
    def parse(self,response):
        print '=====parse_surface_item:=====response:',response
        print 'i'*40

        ##xxoo  = scrapy.Field()
        ##print 'type(xxoo) : ', type(xxoo)  ##  scrapy.item.Field
        ##print 'xxoo : ' , xxoo  

        base_url = get_base_url(response)

        ##===================  item控制器a     =======
        ##################  链接长度统计 #############################
        hrefs=response.xpath('//a/@href').extract()
        ##找出出现最多的那个长度值，以及长度的最长值
        lengths=[]
        for href in hrefs:
            href = urljoin(base_url,href )
            length = len( ''.join(href) )
            lengths.append(length)##链接长度列表

        print 'lengths: ',lengths


        #########################  筛选链接集合###########################
        ##可用链接长度值分为三个阶段：均值分别为：leng_golden，leng_silver，leng_copper
        ##根据 链接长度列表 得到 长度--频度 字典{长度：频率}
        length_frequency = list_2_dict(lengths)  ####  原始字典
        #lamda: 控制系数.控制系数越小，则越松弛。越大则越严格.
        lamda = 0.5   ####
        evalu_length_freq = evaluation(length_frequency , lamda )##评估字典
        print 'evalu_length_freq : ',evalu_length_freq

        list_evalu = evalu_length_freq.keys() ##可用键
        print 'list_evalu : ',list_evalu
        print 'oh, here.'


        #######################  标题-链接搜集   ###############################
        print 'crawl start.'
        ##sites:  筛选出来的"有效的"链接集合
        sites = response.xpath('//a')
        for site in sites :
            ##item['link']
            href = site.xpath( './@href' ).extract()   ##  type(href) :  list
            ##print 'iiiiiiiiiiiiiii  type(href) : ', type(href)
            ##print 'href : ' , href
            href = urljoin( base_url, ''.join( href )  )  ##  type(href) :   str  
            print 'iiiiiiiiiiiiii   : type( href ) : ', type( href  )  #### type:  unicode
            href = s_any_2_utf8(href)

            ##item['manufacturer']
            bu = base_url[7:30]
            if isinstance( bu , str):
                bu = bu.replace(":",'_')
                bu = bu.replace(".",'_')
                bu = bu.replace("/",'_')
                bu = bu.replace('?','_')
                bu = bu.replace('=','_')
                bu = bu.replace('&','_')
                bu = bu.replace('%','_')
                bu = bu.replace('#','_')
            print 'iiiiiiiiiiiiii type( bu ) : manufacture : ', type( bu )
            print 'iiiiiiiiiiiiii bu    : ==   manufacture : ', bu
            manufacturer = bu    ##  type: str   code: utf8 
            
            ##item['title']
            length = len( ''.join( href ) )
            print 'iiii  :  11'
            ##筛子1 ： 首选必须是“有效”链接
            if length in list_evalu :
                print 'iiii  :　　XXXX'
                title = site.xpath('./text() ' ).extract()  ## type: list  code: utf8
                ##print 'iiii  : type(title) :' ,type(title) 
                print 'iiii  : title :' ,title 
                ##筛子2 ： 新闻标题必须有至少一个字符(注： 即便是空字符串也不允许)
                if len(title)!=0:
                    print 'iiii  : title[0] :' ,title[0]
                    title[0] = title[0].replace( '\n', '')
                    title_s = s_any_2_utf8( title[0] )
                    if len(title_s)>18:
                        item = ChinanewsproItem( title=title_s, link=href, manufacturer=manufacturer )
                        print 'iiiiii : 获得item : ' ,item
                        yield scrapy.Request(href,callback=self.parse_body,meta={'item':item})
                    

    ########################################################################################
    ##正文抓取函数
    def parse_body(self,response):
        print 'b'*40
        print '进入正文抓取部分'
        print 'parse_body: create dir-file,write in...'
        print 'parse_body: response: ',response
        item = response.meta['item']
   
        ##item['encode']
        encode_0 = response.xpath('/html/head')
        encode_1 = encode_0.xpath('.//meta')
        encode_3 = ''
        for en in encode_1:
            encode_2 = en.xpath('@content').extract()
            if len(encode_2)!=0:
                encode_2 = encode_2[0]
                if encode_2.find('charset') != -1:
                    encode_3 = encode_2.encode('utf-8')
        encode_3 = encode_3.strip('text').strip('/').strip('html').strip('; ').strip('charset=')
        ##print 'parse_body: head : encode_3 :',encode_3
        item['encode'] =  encode_3      ##  type : str   code: utf8
        ##print 'type( item[\'encode\'] )  :', type(  item['encode'] )
        ##print 'item[\'encode\'] :', item['encode']


        #建立文件保存路径
        ##一级路径: 域名
        ##item['path']
        basic_path = '/data/news_data/all_news/'
        manu = item['manufacturer'][:]
        path_order_one = os.path.join(basic_path, manu)

        ##二级路径：日期
        t = time.localtime()
        date_name = time.strftime('%Y_%m_%d',t)
        path_order_two = os.path.join( path_order_one ,date_name )
        new_path = path_order_two 
  

        ##正文统计分析
        ##正文-标题搜集
        #建立文件名
        file = ''
        hash = 0
        bodys = response.xpath('//body')

        title = bodys.xpath('.//h1/text()  |  ../*[contains(@*,\'titl\')]').extract()

        time_x_1 = bodys.xpath(' .//*[ contains(@*,\'time\') ]'  )

        t_release = []
        t_t = ''
        print 'bbbb    ttttt    1111'
        for xx in time_x_1:
            t_r = xx.xpath(' text() ' ).extract()   #### list
            if len(t_r)>0:
                print 'bbbb    ttttt    2222'
                if isinstance(t_r, list):   ##  是list
                    print 'btbtbt 发布时间  isinstance(t_r,list)  ：',' yes'
                if isinstance(t_r, str):   ##  不是str
                    print 'btbtbt 发布时间  isinstance(t_r,str)  ：',' yes'
                for tt in t_r:
                    print 'btbtbt ,  发布时间  type(tt)  : ', type(tt)  #### 居然是  unicode  !!!!!!
                    if isinstance(tt, list):   ####不是 list
                        print 'btbtbt 发布时间  isinstance(tt,list)  ：',' yes'
                    if isinstance(tt, str):   ####  不是str
                        print 'btbtbt 发布时间  isinstance(tt, str)  ：',' yes'
                        a =  s_any_2_utf8( tt  )
                        t_t += a
                    if isinstance( tt , unicode) :
                        a = tt.encode('utf8')
                        t_t += a
                    ##if isinstance(t,str):
                    ##    print 'bbbb    ttttt    3333'
                    ##    tc += t
                t_release.append( t_r[0] )         ####   type(time_release ):str  encode: unicode  
        ##time_release = list_evaluation( t_release )   

        #time_release = s_any_2_utf8(  time_release  )

        if len( title ) != 0:
            title_a = title[0]  ##   title就取第一个!!!!!!!!!!!!!.  
            ####  暂不考虑和目录中的标题相一致
            ##if isinstance( title, str ):
            ##    title_a = title
            ##if isinstance( title,list ):
            #    for t in title:
            #        if isinstance(t,str):
            #            title_a += t
            sha1obj = hashlib.sha1()
            sha1obj.update( title_a )
            hash = sha1obj.hexdigest()
            print 'hash: ',hash
            file = new_path+'/'+hash##hash 值作为文件名
            item['path'] = new_path    ##  type: str  code: utf8
            item['hash'] = hash   ####  type: str code: urf8

            ##开始写一个文本
            path_check = '/data/news_data'
            ##crawl_body.file_check: 检查文件在既有文件夹下是否已经存在.如果已经存在,还要判断其是否异常。
            ##返回值 1: 存在且正常. 
            ##       0: 不存在  
            ##       2: 异常.
            pl = file_check_function.hash_check(  path_check , hash  )
            print 'pl : ', pl
            pl = 0 ##  无条件抓取。
            if pl != 1:   ##有条件抓取正文
                ##获取标题、取hash值
                ##获取新闻发布时间、写入发布时间
                ##item['time_release'] = time_release  # type: str  encode: unicode 
                item['time_release']  = t_t

                ##抓取正文
                bodys_b = bodys.xpath('.//p')
                main_bodys = []
                print 'bbbbbbbbbbbb  : 要抓main_bodys ........'
                for bd in bodys_b:
                    body = bd.xpath('text()').extract()
                    if ( len(body) != 0  ) :
                        if len(body[0]) >20:   ####至少6个汉字
                            bb = s_any_2_utf8( body[0]   )
                            ##-------------------------------
                            if isinstance(bb, str):     ##是str类型
                                print 'isinstance(bb, str)  : yes'
                            if isinstance(bb, unicode):
                                print 'isinstance(bb, unicode)  : yes'  ##不是Unicode编码
                            else:
                                vv = chardet.detect(bb) ##if isinstance(bb, unicode):
                                print 'chardet.detect(bb) :', vv    ##检测得知是utf8编码
                            ##-------------------
                            main_bodys.append( bb )
                        #if isinstance( body, str):
                        #    body = s_any_2_utf8( body   )
                        #    main_bodys.append(body)
                        #    print 'bbbb : ',body
                        #if isinstance( body, list ):
                        #    for b in body:
                        #        if isinstance( b, str):
                        #            body += b
                        #            main_bodys.append(body)
                        #            print 'bbbb : ', body
                item['mainbody'] = main_bodys
   
                ##print '=> => : \n' ,'item = : \n',item

                print 'finish.'
                print '\n\n\n\n'
                return item
    
            else:
                print 'parsing_body : pl : ',pl 
                print '由于文件已经存在.无操作。'
    
        else:
            print '标题为空。不操作。'
    
    
##将列表ls写入文件file中。
##ls[0]:str
def write_ls(ls,file):
    if os.isfile(file):
        os.remove( file )
    fp = open( file,'w'  )
    for l in ls:
        fp.write( l  )
    fp.close()


