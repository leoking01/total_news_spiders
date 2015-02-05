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
import sys
sys.path.append('/home/luokun/work/scrapy_projects/sinanews/sinanews/spiders')
from  check import  file_check
import crawl_body
sys.path.append('/home/luokun/work/scrapy_projects')
from common_functions import *

fp_d = open('hash_diff.txt','w')
fp_s = open('hash_same.txt','w')

class SinanewsPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='db_luokun',
            user='root', passwd='', cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        if len( item['title'] ) == 0 or len( item['mainbody'] ) == 0 :
            return 
        if len(item['title'])!=0:
            ##  一、 数据库处理
            ##part 1 : 数据库处理
            re = tx.execute("select * from baidunews  where hash = %s ", (item['hash'][0], ))
            re += tx.execute("select * from qqnews  where hash = %s ", (item['hash'][0], ))
            re += tx.execute("select * from sinanews  where hash = %s ", (item['hash'][0], ))
            re += tx.execute("select * from chinanews  where hash = %s ", (item['hash'][0], ))
            tt = datetime.datetime.now()
            print 'type(tt): ',type(tt)
            if re:
                log.msg("Item has already been stored in db: %s" % item, level=log.DEBUG)
                fp_s.write('hash_present: ')
                fp_s.write( item['hash'][0] )
                fp_s.write( '\n' )
            else:
                if  len( item['hash'] ) == 0:
                    item['hash']=['']
                print 'pipline: time_release: ',item['time_release']
                if  len( item['time_release'] ) == 0:
                    item['time_release']=['']

                tx.execute( "insert into sinanews(title, link, response_news, time_release, time_add, hash, manufacturer)"
                            " values(%s,%s,%s,%s,%s,%s,%s)" ,(item['title'][0],
                                item['link'],
                                item['response_news'],
                                item['time_release'] ,
                                tt,
                                item['hash'],
                                item['manufacturer']
                                 )   )
                print 'db_store: title: ',''.join(item['title'][0]).encode('utf-8')
                print 'ok????'

                fp_d.write('hash_present: ')
                fp_d.write( item['hash'][0] )
                fp_d.write( '\n' )
                log.msg("Item is storing in db : %s" % item, level=log.DEBUG)


            ## 二、数据文件处理
            #建立文件路径
            old_path='/data/news_data/sina_news/'
            hash = item['hash'][0]
            check_path = '/data/news_data'
            pl = crawl_body.file_check( check_path, hash)
            ##pl = 0
            if pl == 1:
                return 
            else :
                pass 
            t=time.localtime()
            t=time.strftime('%Y_%m_%d',t)
            new_path = os.path.join(old_path,t)
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
            #建立文件名
            file = new_path+'/'+''.join( item['hash'][0] )
            fileoper = open(file,'w')
            fileoper.write('title:\n')
            fileoper.write( item['title'][0]  )
            fileoper.write('link:\n')
            fileoper.write( item['link'][0]  )
            fileoper.write('\ntime_release:\n'  )
            fileoper.write( ''.join(item['time_release']) )
            fileoper.write('\nlink:\n')
            fileoper.write( ''.join(item['link'][0]) )
            fileoper.write('\nmainbody:\n')
            print 'pipeline:  item[\'mainbody\'] :',item['mainbody']
            bodys = item['mainbody']
            for bd in bodys:
                u(bd , 'utf8')
                fileoper.write( bd )
                fileoper.write( '\n' )
            fileoper.close()
                     
    def handle_error(self, e):
        log.err(e)
                                              


