#! coding: utf-8
##文件检查函数: 检查文件是否在某路径下存在.
##参数path: 路径
##    hash: 哈希值，即文件名
##返回值：0 -- 文件不存在
##        1 -- 文件已经存在
import os


def file_check(path,hash):
    dirs_base=path
    dirs_main=os.listdir(dirs_base)
    state=0
    print '******   main_directors list:  ******'
    print dirs_base,' :'
    print dirs_main

    for d in dirs_main:
        dir_0='/data/news_data/'+d
        print '\n'
        print '******   dir_0 = ',dir_0,'   ******'
        for dir_a in os.listdir(dir_0):
            dir_b=dir_0+'/'+dir_a
            print 'The number of files in ', dir_b, ' is: ',len( os.listdir(dir_b) )
            for file in os.listdir(dir_b):
                if hash==file:
                    state=1
                    print 'found: 文件 %s 存在于文件夹 %s 中.' %(hash,dir_b)
                    return state
                else:
                    state=0
    print 'finish.'
    return state
    
    


