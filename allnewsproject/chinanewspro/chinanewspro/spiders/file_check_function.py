#! /usr/bin/python
# -*- coding: utf-8 -*-
## 函数1 parse_body ： 暂无用 。 类函数。
## 函数2 file_check :  检查文件是否在路径中存在。全局函数

import os,sys
import hashlib
import datetime,time
    
    
##文件检查函数: 检查文件是否在某路径下存在.
##参数path: 路径
##    hash: 哈希值，即文件名
##返回值：0 -- 文件不存在
##        1 -- 文件已经存在
##dirs_base='/data/news_data/all_news'
##dir_0 = ./manu
##dir_b = ./datetime
def file_check(dirs_base,hash):
    dirs_main = os.listdir(dirs_base)
    state = 0

    for d in dirs_main:
        dir_0 = dirs_base+'/'+d
        if os.path.isdir(dir_0):
            for dir_a in os.listdir(dir_0):
                dir_b=dir_0+'/'+dir_a
                ##如果dir_b 是文件夹
                if os.path.isdir(dir_b):
                    for file in os.listdir(dir_b):
                        if hash==file:
                            state = 1
                            v=os.path.getsize(dir_b+'/'+''.join(file) )
                            if v<400:
                                state = 2
                                ##print '文件虽然存在但有异常(文件过小,可能是假新闻.)a'##all_news
                            else:
                                ##print '文件是正常的.b'
                                pass
                            return state
                        else:
                            pass
                ##如果dir_b是文件
                elif os.path.isfile(dir_b):
                    if hash==dir_a:
                        state = 1
                        v=os.path.getsize(dir_b )
                        if v<100:
                            state = 2
                            pass
                            ##print '文件虽然存在但有异常(文件过小,可能是假新闻.)c'##百度新闻、新浪、等新闻的
                        else:
                            ##print '文件是正常的.d'
                            pass
                        return state
                    else:
                        pass
        else:
            if hash==dir_0:
                state = 1
                v=os.path.getsize(dir_0 )
                if v<100:
                    state = 2
                    print '文件虽然存在但有异常(文件过小,可能是假新闻.)e'#### 实际不会使用的
                else:
                    print '文件是正常的.f'
                    pass
                return state
            else:
                pass
    return state
    

####   
def news_data_check(dirs_base,hash):
    dir_base = os.listdir(dirs_base)
    state = 0
    for dir in dir_base:
        path_t = dirs_base+'/'+dir
        state = file_check(path_t,hash)
        if state!=0:
            return state

    return state


####检查路径folder 下是否已经有hash文件存在.
def hash_check(folder,* hash):
    ind = 0
    for f in os.walk(folder ):
        ##print 'f[0] : ', f[0]  ## 
        if hash[0] in f[2]:
            ind += 1
            break
    return ind
                


###################################################
def test(folder):
    for f in os.walk(folder ):
        ##f    :                      : tuple
        ##f[0] : 当前路径             : str
        ##f[1] ：当前路径下的文件夹   : []
        ##f[2] ：当前路径下的文件列表 : []
        print 'f          : ',f 
        print 'type(f)    : ',type(f)
        print 'type(f[0]) : ',type(f[0])
        print 'type(f[1]) : ',type(f[1])
        print 'type(f[2]) : ',type(f[2])
                
###################################################
xx = """
##f = '/data/news_data/qq_news'
f = '/data/news_data/'
##test(f)

hash = '3e72e059cab1082176179ed9e2c289ccff1ef7cb'
hash = '3e72e059cab1082176179ed9e2c289ccff1ef7ci'
print '路径为 :  ' ,f
print '待检查的hash值为 : ',hash
print '检查结果 : ',hash_check(f, hash)
"""












