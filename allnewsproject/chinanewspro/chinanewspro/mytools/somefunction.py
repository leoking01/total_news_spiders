#!/usr/bin/python
#! coding=utf-8 
import sys,os,time,datetime
import shutil

#####
####这不明白这个函数哪里有问题，但是它确实有问题。
##修改时间： 2015-1-23
def get_filename( dirs,all_filenames,all_hashs ):
    for dd  in os.listdir( dirs ):
        ob  = os.path.join( dirs, dd )
        if os.path.isdir( ob ):
            get_filename( ob , all_filenames,all_hashs)
        elif os.path.isfile( ob ):
            all_filenames.append( ob  )
            all_hashs.append( dd  )
        else:
            pass
    ##return all_filenames

####
####
##修改时间： 2015-1-23
def hashs_division( hashs_all, hashs_basic ):
    if len( hashs_all ) == 0:
        return ##pass ##break
    pp = """
    for hash in hashs_all:
        if len(hashs_basic)==0:
            hashs_basic.append(hash)
        else:
            pass
        indi = 0
        for ha in hashs_basic:
            if ha == hash:
                indi += 1
                break
        if indi == 0:
            hashs_basic.append(hash)
    """
    for h in hashs_all:
        ##if len( hashs_basic  ) == 0:
        ##    ##hashs_basic.append(h)
        ##else:
        ##    pass
        if h in hashs_basic :
            pass 
        else:
            hashs_basic.append( h )


##修改时间： 2015-1-23
######  !!!!提取无重复文件名单.只适合以新闻标题hash值命名的情形. 
def files_division(file_all,hash_basic, file_basic):
    dcfa = {}.fromkeys(file_all,   0 )  ##
    repeated_files = []
    if len(file_all)==0 or len(hash_basic)==0:
        return {}
    for h in hash_basic:
        hash = h
        indicater = 0
        for d in dcfa.keys():
            if h in d[-40:]:
                indicater += 1
                dcfa[d] = indicater
                ##break 
    
    for d in  dcfa.keys():
        if dcfa[d] == 1:
            file_basic.append( d )
        if dcfa[d] >1:
            repeated_files.append( d )

    ##return  dcfa ##file_basic
    return  repeated_files  ##  返回重复文件集
        




#######
#从总文件列表file_all中删除重复项。
## 规则： 不在file_basic 中的酒删除(实际转移到另外一个路径下.但有覆盖情况.)
## modified datetime: 2015-1-23
def delete_repeated_files(file_all,file_basic):
    repeatedfiles_store = '/data/repeatedfiles_store'
    if not os.path.isdir( repeatedfiles_store ):
        os.mkdir(  repeatedfiles_store  )
    for file in file_all:
        if not file in file_basic:
            shutil.copy(file,repeatedfiles_store )
            os.remove( file  )
            ##delete_pro=open('deleted_files20150123.txt','a')
            ##delete_pro.write( str(file) )
            ##delete_pro.write( '\n' )
            ##delete_pro.close()##希望这个文件永远为空.
            ##os.remove(file)####终于不用再注释这一行了
    pass


####
def delete_file(path,characteristic):
    ##example: 
    ##      path = '/data/news_data'
    ##      characteristic = '2015_01_10'
    allfiles,allhashs = [],[]
    get_filename(path,allfiles,allhashs)
    for file in allfiles :
        if file.find(characteristic) != -1:
            os.remove(file)
    pass


## 空 文件夹获取
## 用于空文件夹删除
def get_dirs_names( dirs,all_dirnames ):
    content = os.listdir(dirs)
    if len(content) == 0:   ##为空
        all_dirnames.append(dirs)
    else:
        for dir in content:
            dir_0 = dirs+'/'+dir
            if os.path.isdir(dir_0):   ##有文件夹
                get_dirs_names(dir_0,all_dirnames)
            elif os.path.isfile(dir_0):    ## 有文件
                pass
            else:
                pass
    return all_dirnames   




##  invalid data clear:
##              ==
##              清理无效文件
##  bad urls: 文件body为空。  
##  无效文件： body部分不足200
def get_invalid_files_urls( dirs, all_filenames, all_hashs, badfiles ):
    ##all_files = get_filename( dirs,all_filenames,all_hashs )
    get_filename( dirs,all_filenames,all_hashs )
    all_files = all_filenames[:]
    ## 筛选文件:找出invalid files。
    ##badfiles = []
    for f in all_files:
        if os.path.getsize(f)< 300 :
            badfiles.append(f)
    ##pass
    ##取出所有bad urls，并返回。
    urls = []
    for f in badfiles:
        fp = open(f,'r')
        ct = fp.readlines()
        for it in ct:
            if it.find('http')!= -1:
                urls.append(it)
    return urls








