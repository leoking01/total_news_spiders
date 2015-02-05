# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import  os
from os import path
import datetime,sys,time
import hashlib

from twisted.enterprise import adbapi
import MySQLdb.cursors
import MySQLdb

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log

sys.path.append('/home/luokun/work/svn_103_scrapy_projects/allnewsproject/chinanewspro/chinanewspro/spiders')
from chinanews_functions import  list_2_dict,bianli,dict_max,dict_min,dict_modif,evaluation,dir_creat,list_evaluation
import file_check_function

##fp_s = open('scrapy_pipeline_indicater_same.txt','a')
##fp_d = open('scrapy_pipeline_indicater_diff.txt','a')
sys.path.append('/home/luokun/work/svn_103_scrapy_projects/common_functions')
from functions import  s_any_2_encoding, s_any_2_utf8

##reload( sys )
##sys.setdefaultencoding( 'utf8' )
def any_2_str(any):
    if len(any) == 0:
        return ''
    if isinstance(any , list):
        return any[0]
    if isinstance(any, str):
        return any
#id = 0
####
class ChinanewsproPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='news_collection',
            user='luokun', passwd='', cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item


    ##处理抓取来的数据:
    ##  1. 数据库处理
    ##  2. 文件写入和保存
    def _conditional_insert(self, tx, item):
        print 'p'*40
        print 's'*40
            
        ##                  ====  item控制器b     =======
        ##依据文件名进行检查
        ##item检查:       标题、发布时间、正文、encode
        ##                异常的item的链接将被写入异常报告文件item_exception.txt，并给出异常编号.
        ##          标题异常    0    >18   即6个汉字
        ##          时间异常    0    暂不严格要求
        ##          正文异常    0    >100  即33个汉字
        ##          编码异常    0    暂不严格要求
        ##  ------------------
        if isinstance(item['title'],str):   ## 是str 类型
            print 'pspspsps : isinstance(item[\'title\'],str) ' , 'yes'
        if isinstance(item['title'],list):  ## 不是 list类型
            print 'pspspsps : isinstance(item[\'title\'],list) ' , 'yes'
        ##  -----------

        
        ##丢弃文章记录:diuqi_xinwen_mark.txt
        fp = open('diuqi_xinwen_mark.txt','a')
        id = 0
        ##对标题作检查: 无标题者，丢弃。
        if len( item['title'] ) != 0:
            title = item['title']
            title = s_any_2_utf8( title )
            ##标题字数小于2的新闻被丢弃
            if len(title) < 18:
                mess = 'error_number: 001  error: 新闻标题小于6个汉字。(直接)丢弃。'
                print mess 
                id += 1
                fp.write( 'id: ' )
                fp.write(  str(id)  )
                fp.write( '\n' )
                fp.write( 'title: ' )
                if len( item['title'] ) != 0:
                    fp.write( item['title'] )
                fp.write( '\n' )
                fp.write( 'link: ' )
                fp.write( item['link'] )
                fp.write( '\n' )
                fp.write( mess )
                fp.write( '\n' )
                fp.write( '\n' )
                ##fp.close()
                return 

        ##对正文字数作检查: 无正文者，丢弃。
        if len( item['mainbody'] ) == 0:
            mess = 'error_number: 002 error:  新闻正文为零(尽管标题合乎要求)。丢弃。'
            print mess 
            id += 1
            fp.write( 'id: ' )
            fp.write(  str(id)  )
            fp.write( '\n' )
            fp.write( 'title: ' )
            if len( item['title'] )!= 0:
                fp.write( item['title'] )
            fp.write( '\n' )
            fp.write( 'link: ' )
            fp.write( item['link'] )
            fp.write( '\n' )
            fp.write( mess )
            fp.write( '\n' )
            fp.write( '\n' )
            ##fp.close()
            return 

        ##过少: 正文字数过少者，丢弃
        if len( item['mainbody'] ) != 0:
            mainbody = item['mainbody']
            max_len = 0
            for bd in mainbody:
                if len(bd) > max_len :
                    max_len = len(bd)
            ##正文段落最大字数小于60个字的新闻被丢弃
            ##200 : 60个字符.
            if max_len < 50:
                mess = 'error_number: 003 error:  新闻正文段落最大字数不够16字(尽管既有标题，也有正文.)。丢弃。'
                print mess 
                id += 1
                fp.write( 'id: ' )
                fp.write(  str(id)  )
                fp.write( '\n' )
                fp.write( 'title: ' )
                if len( item['title'] )!= 0:
                    fp.write( item['title'] )
                fp.write( '\n' )
                fp.write( 'link: ' )
                fp.write( item['link'] )
                fp.write( '\n' )
                fp.write( mess )
                fp.write( '\n' )
                fp.write( '\n' )
                ##fp.close()
                return
        

        ##依据标题进行后处理
        lt = item['title']
        lh = item['hash']
        eh , et = 0, 0
        print 'pppp     uuuuuuuu'
        et = len(lt)
        eh = len(lh)
        #*************************************
        #*************************************
        #******   数据存储前的总的判断   ***** 
        #*************************************
        #   (1) 标题hash有值                 *
        #   (2) 标题title字数不少于6         *
        #*************************************
        #*************************************
        #c5b743769c37df115128036ae52d4fd9d2a2d215
        if eh == 40 and et >20:
            print 'nnnnnn  1111 '
            ##part 1 : 数据库保存
            ##============================================================
            ##==========      第一个检查： 记录是否存在   ================
            ##============================================================
            ##re  = tx.execute("select * from baidunews  where hash = %s ", (item['hash'][0], ))
            ##re += tx.execute("select * from qqnews     where hash = %s ", (item['hash'][0], ))
            ##re += tx.execute("select * from sinanews   where hash = %s ", (item['hash'][0], ))
            re = 0   
            re += tx.execute("select * from china_news  where hash = %s ", ( lh , ))
            ##条件判断
            if re != 0 :
                ##如果数据库中已经有了这个新闻标题就不会再次写入数据库
                print 'nnnnnn  0000 '
                log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
            else:
                ##数据库中没有这个新闻标题，将写入数据库。
                print 'nnnnnn  2222 '
                t = datetime.datetime.now()
                t = t.strftime("%Y-%m-%d_%H:%M:%S")

                tx.execute( "insert into china_news(title,link,time_release,time_add,hash,manufacturer,path,encode)"
                    "values(%s,%s,%s,%s,%s,%s,%s,%s)" , (item['title'], item['link'], item['time_release'] ,t, item['hash'],item['manufacturer'], item['path'], item['encode'] )   )

                print 'ptptpttptptpt   item  保存完成.'

                print '\n\n\n\n'
                log.msg("Item stored in db: %s" % item, level=log.DEBUG)


            ##part 2 : 数据文件保存
            ##pl = file_check_function.news_data_check(path_check,hash)
            ##============================================================
            ##==========      第二个检查： 文件是否存在   ================
            ##============================================================
            hash = item['hash']
            path_check = '/data/news_data'
            pl = file_check_function.hash_check( path_check, hash )
            ##pl = 0##无条件写入
            print 'pp  write? pl:  ',pl
            if pl != 1:
                print 'pp   write?    0000  '
                #建立文件保存路径
                ##一级路径: 域名
                basic_path = '/data/news_data/all_news/'
                path_order_one = dir_creat( basic_path, item['manufacturer']  )

                ##二级路径:日期
                t = time.localtime()
                date_name = time.strftime('%Y_%m_%d', t)
                path_order_two = dir_creat(path_order_one, date_name )
                new_path = path_order_two 
  

                #建立文件名
                file = os.path.join( new_path,  item['hash']   )

                ##打开
                fileoper = open(file,'w')


                ##========新闻内容==========
                ##标题
                fileoper.write('title:\n')
                fileoper.write(  item['title']   )
                fileoper.write(  '\n'  )

                ##发布时间
                ## 在抓取时，time_release 是一个长列表
                fileoper.write('time_release:\n'  )
                if len( item['time_release']    ) != 0:
                    fileoper.write(  item['time_release']  ) 
                    fileoper.write(  '\n'  )

                ##链接
                fileoper.write('link:\n')
                fileoper.write(  item['link']   )
                fileoper.write(  '\n'  )

                ##正文
                fileoper.write('mainbody:\n')
                bb =  item['mainbody']
                for bod in bb:
                    if len( bod ) != 0:
                        fileoper.write(  bod  )
                        fileoper.write(  '\n'  )
                fileoper.close(  )
                print '新闻文件保存成功.  OH YE !!!'     
            
        else:
            ##‘新闻不符合保存条件：即新闻hash缺少，或者标题字数过少。’
            mess =  'error_number: 004  新闻不符合保存条件：即新闻hash缺少，或者标题字数过少。'
            print  mess
            fp.write('title: ')
            fp.write( item['title'] )
            fp.write('\n')
            fp.write('link: ')
            fp.write( item['link'] )
            fp.write('\n')
            fp.write( mess )
            fp.write('\n')
            fp.write('\n')
    

                     
    def handle_error(self, e):
        log.err(e)


    ##自定义哈希函数
    def hash_my(tx):
        pass
                                              
                                              
                                              
    def normalize( ls ):
        if not isinstance(ls, list):
            return ['']
        if len( ls )  == 0:
            ls = ['']
                      
