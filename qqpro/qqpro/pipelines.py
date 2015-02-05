# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from twisted.enterprise import adbapi
import datetime,time
import MySQLdb.cursors

import MySQLdb

from scrapy import log
import hashlib


import sys 
sys.path.append('./spiders')
import crawl_body
from crawl_body import file_check

sys.path.append('/home/luokun/work/scrapy_projects')
from common_functions import u, utf_p 

fp_s = open('hash_same.txt', 'w')
fp_d = open('hash_diff.txt', 'w')


class QqproPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='db_luokun',
            user='root', passwd='', cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item


    def _conditional_insert(self, tx, item):
        re=0
        now=datetime.datetime.now()

        ##确定文件名
        ##title_a=['']
        if len(item['title'])!=0:
            ##part 1 : 数据库处理
            re = tx.execute("select * from baidunews  where hash = %s ", (item['hash'][0], ))
            re += tx.execute("select * from qqnews  where hash = %s ", (item['hash'][0], ))
            re += tx.execute("select * from sinanews  where hash = %s ", (item['hash'][0], ))
            re += tx.execute("select * from chinanews  where hash = %s ", (item['hash'][0], ))
            ##title_a = ''.join(  item['title'][0]  ).encode('utf-8')##!!必须采用严格的格式要求，保持一致
            ##条件判断
            if re != 0 :
                ##如果数据库中已经有了这个新闻标题就不会再次写入数据库
                log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
                fp_s.write('hash_present: ')
                fp_s.write( item['hash'][0] )
                fp_s.write( '\n' )
            else:
                fp_d.write('hash_present: ')
                fp_d.write( item['hash'][0] )
                fp_d.write( '\n' )
                if 1==1:
                    t = datetime.datetime.now()
                    tx.execute( "insert into qqnews(title,link,response_news,time_release,time_add,hash,manufacturer,path ,encode)"
                            " values(%s,%s,%s,%s,%s,%s,%s,%s, %s)" ,(item['title'][0], item['link'],item['response_news'],item['time_release'] ,t,item['hash'],item['manufacturer'],item['path'], item['encode'] )   )
                    print 'db_store: title: ',''.join(item['title'][0]).encode('utf-8')
                    log.msg("Item stored in db: %s" % item, level=log.DEBUG)
            

            path = '/data/news_data'
            hash = item['hash']
            pl = crawl_body.file_check(path,hash)
            if pl != 1:
                #建立文件路径
                old_path='/data/news_data/qq_news/'
                t=time.localtime()
                t=time.strftime('%Y_%m_%d',t)
                new_path=os.path.join(old_path,t)
                if not os.path.isdir(new_path):
                    os.mkdir(new_path)
                        
                #建立文件名
                file = new_path+'/'+''.join( item['hash'] )
                fileoper = open(file,'w')
                fileoper.write('title:\n')
                u( item['title'][0] ,'unicode' )
                utf_p( item['title'][0] ,'utf8' )
                fileoper.write( item['title'][0]  )
                fileoper.write('\ntime_release:\n'  )
                fileoper.write( ''.join(item['time_release']) )
                fileoper.write('\nlink:\n')
                fileoper.write( ''.join(item['link']) )
                fileoper.write('\nmainbody:\n')
                bodys = item['mainbody']
                for bd in bodys:
                    u( bd,unicode )
                    ##utf_p( bd,'utf8' )
                    fileoper.write( bd   )
                fileoper.close()
                     

                     
    def handle_error(self, e):
        log.err(e)


    ##自定义哈希函数
    def hash_my(tx):
        pass

xx = """
def u(s,encoding): 
    if isinstance(s,unicode):
        return s
    else:
        return unicode(s,encoding )
                                              
def utf_p(s,encoding): 
    if isinstance(s,utf8):
        return s
    else:
        return unicode(s,encoding )
"""                                              
                                              
