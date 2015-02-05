#!/usr/bin/python
import os

#dirs=os.listdir('/data/news_data/sina_news/')
#print 'director list: \n',dirs


#for d in dirs:
#    dire='/data/news_data/sina_news/'+d
#    print 'The number of files in ', dire, ' is: ',len( os.listdir(dire) )
#print 'finish.'




dirs_base='/data/news_data/'
dirs_main=os.listdir(dirs_base)
print '******   main_directors list:  ******'
print dirs_base,' :'
print dirs_main

for d in dirs_main:
    dir_0='/data/news_data/'+d
    print '\n'
    print '******   dir_0 = ',dir_0,'   ******'
    for dir_a in os.listdir(dir_0):
        #print 'dir_a = ',dir_a
        dir_b=dir_0+'/'+dir_a
        print 'The number of files in ', dir_b, ' is: ',len( os.listdir(dir_b) )
print 'finish.'












