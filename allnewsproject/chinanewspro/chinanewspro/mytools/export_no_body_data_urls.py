#! /usr/bin/python
#! coding:utf-8

import os
import sys
import somefunction

def gen_badurls( dirs, all_filenames, all_hashs, badfiles ):
    all_files = somefunction.get_filename( dirs,all_filenames,all_hashs )
    ##badurls = somefunction.get_dirs_names(path,bad_urls)
    ##print 'len of bad_urls: ',len( bad_urls )
    #pf = open('badurls.txt','w')
    #for ct in bad_urls :
    #    pf.write( ct )
    #    pf.write( '\n' )
    ## 筛选文件
    ##badfiles = []
    for f in all_files:
        if os.path.getsize(f)<220:
            badfiles.append(f)
    ##pass
    ##取出所有urls
    urls = []
    for f in badfiles:
        fp = open(f,'r')
        ct = fp.readlines()
        for it in ct:
            if it.find('http')!= -1:
                urls.append(it)

    return urls
    

dirs = '/data/news_data'
all_filenames = []
all_hashs = []
badfiles = []
urls = gen_badurls( dirs, all_filenames, all_hashs ,badfiles)
print 'len(urls): ',len(urls)
fp = open('bad_urls_no_body.txt','w')
for u in urls:
    fp.write(u)
    ##fp.write('\n')
fp.close()


bdfp = open('badfiles_nobody.txt','w')
for u in badfiles :
    bdfp.write(u)
    bdfp.write('\n')
bdfp.close()

