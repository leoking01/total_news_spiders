# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys, os
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from twisted.enterprise import adbapi
import datetime,time
import MySQLdb.cursors

sys.path.append('/home/luokun/work/scrapy_projects/baidu/baidu/spiders')
import crawl_body
import MySQLdb

from scrapy import log
sys.path.append('/home/luokun/work/scrapy_projects')
from common_functions import u , utf_p

sys.path.append('/home/luokun/work/scrapy_projects')
from common_functions import *

fp_s = open('hash_same.txt','w')
fp_d = open('hash_diff.txt', 'w')

class BaidunewsPipeline(object):
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
        if len(item['title'])!=0:
            ##part 1 : 数据库处理
            re = tx.execute("select * from baidunews  where hash = %s ", (item['hash'][0], ))
            re += tx.execute("select * from qqnews  where hash = %s ", (item['hash'][0], ))
            re += tx.execute("select * from sinanews  where hash = %s ", (item['hash'][0], ))
            re += tx.execute("select * from chinanews  where hash = %s ", (item['hash'][0], ))
            ##title_a = ''.join(  item['title'][0]  ).encode('utf-8')##!!必须采用严格的格式要求，保持一致
            ##数据库处理
            result = tx.fetchone()
            if re:
                log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
                fp_s.write('hash_present: ')
                fp_s.write( item['hash'][0] )
                fp_s.write( '\n' )
            else:
            ##条件写入数据库
                tx.execute("insert into baidunews (title,link,time_release,time_add, hash,manufacturer,path,encode) "
                    "values (%s,%s,%s,%s, %s,%s ,%s, %s)",
                    (item['title'],item['link'],item['time_release'],datetime.datetime.now(),item['hash'],item['manufacturer'],item['path'], item['encode'])
                )
                fp_d.write('hash_present: ')
                fp_d.write( item['hash'][0] )
                fp_d.write( '\n' )
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)
            
            ##数据文件保存
            ##以标题hash为标准
            path = '/data/news_data'
            hash = item['hash'][0]
            pl = crawl_body.file_check(path,hash)
            ##条件保存: 仅当数据文件不正常的时候写入数据、或者重写数据
            ##pl:0 : 文件不存在  
            ##   1 ：正常  
            ##   2 ：存在，但是过小
            if pl != 1 :
                #建立文件路径
                old_path='/data/news_data/baidu_news/'
                t=time.localtime()
                t=time.strftime('%Y_%m_%d',t)
                new_path = os.path.join(old_path,t)
                if not os.path.isdir(new_path):
                    os.mkdir(new_path)
                #建立文件名
                file = new_path+'/'+''.join( item['hash'] )
                fileoper = open(file,'w')
                fileoper.write('title:\n')
                fileoper.write( item['title'][0]  )
                fileoper.write('\ntime_release:\n'  )
                fileoper.write( ''.join(item['time_release']) )
                fileoper.write('\nlink:\n')
                fileoper.write( ''.join(item['link']) )
                fileoper.write('\nmainbody:\n')
                ##fileoper.write( ''.join(item['mainbody']) )
                if len( item['mainbody'] ) >= 1:
                    for bod in item['mainbody']:
                        bod = u(bod, unicode )
                        bod = bod.encode('utf8')
                        fileoper.write(  bod  )
                fileoper.close()
                     

            print '\n\n\n\n'
                     
    def handle_error(self, e):
        log.err(e)
                                              


