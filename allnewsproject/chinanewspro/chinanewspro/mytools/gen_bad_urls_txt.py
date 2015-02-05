#! /usr/bin/python
#! coding:utf-8

import os  , shutil 
import somefunction

def gen_badurls(path,bad_urls):
    badurls = somefunction.get_dirs_names(path,bad_urls)
    print 'len of bad_urls: ',len( bad_urls )
    #pf = open('badurls.txt','w')
    #for ct in bad_urls :
    #    pf.write( ct )
    #    pf.write( '\n' )
    #pf.close()
    pf = open('badurls2.txt','w')
    for ct in badurls :
        pf.write( ct )
        pf.write( '\n' )
    pf.close()
    #####删除空文件夹
    pl = 0
    for dir in bad_urls:
        pl = len ( os.listdir(dir)  )
        if pl == 0:
            ##shutil.rmtree(dir)  删除空路径！！！
            pass

path = '/data/news_data/'
##    '/data/news_data/all_news/'
bad_urls = []
gen_badurls(path,bad_urls)

