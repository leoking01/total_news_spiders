#! /usr/bin/python
# -*- coding:utf8 -*-
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')

import chardet
import shutil

####将字符串s转成编码encoding形式
## s_any_2_encoding： 任意编码转任意编码 
def s_any_2_encoding(s, encoding):
    if isinstance(s,unicode):
        s = s.encode( encoding )

        return s
    else:
        cod = chardet.detect(s)['encoding']
        s = s.decode(  cod )
        s = s.encode( encoding )
        ##s = unicode(s,encoding)
        return s

## s_any_2_encoding： 任意编码转utf8 
def s_any_2_utf8(s):
    if isinstance(s,unicode):
        s = s.encode('utf8')
        return s
    else:
        cod = chardet.detect(s)['encoding']
        s = s.decode(  cod )
        s = s.encode( 'utf8' )
        ##s = unicode(s,encoding)
        return s


###################################################

def test(s):
    print '默认编码格式为：', sys.getdefaultencoding()

    cod = chardet.detect(s)['encoding']
    print 's的编码格式为: ', cod ##chardet.detect(s)['encoding']
    
    ## s_any_2_encoding： 任意编码转任意编码 
    s = s_any_2_encoding(s,'utf8')
    cod = chardet.detect(s)['encoding']
    print 's的编码格式为: ', cod ##chardet.detect(s)['encoding']
    
    s = s_any_2_encoding(s,'gbk')
    cod = chardet.detect(s)['encoding']
    print 's的编码格式为: ', cod ##chardet.detect(s)['encoding']
    
    s = s_any_2_encoding(s,'gb2312')
    cod = chardet.detect(s)['encoding']
    print 's的编码格式为: ', cod ##chardet.detect(s)['encoding']

    ## s_any_2_encoding： 任意编码转任意编码 
    s = s_any_2_utf8(s)
    cod = chardet.detect(s)['encoding']
    print 's的编码格式为: ', cod ##chardet.detect(s)['encoding']

    print '\n'

###################################################
sss = """
s = '中国人,一群很多的。'
test(s)

d = 'http://www.baidu.com/s?wd=python%20unicode%E5%87%BD%E6%95%B0&ie=utf-8&f=8&rsv_bp=1&tn=monline_4_dg&rsv_pq=96c329050000b01c&rsv_t=74c1zvCNtoBq2xnNsGYdnj44oZSVVtZQyizpYO5d%2BMPdoZKjb9SdjyBFt8tMQLIKtxlF&bs=python%20unicode%28%29'
test(d)
d = 'links:'
test(d)
"""

###################################################

def delete_special_folders(path,* character):
    fp = open('log.txt','w')
    ##print type(character)
    ##print character
    mywalk = os.walk(path)
    n = 0
    for m in mywalk:
        ##print m[0]
        ##print type( m[0] )
        if character[0] in m[0]:
            if os.path.isfile(m[0]):
                os.remove( m[0]  )
                fp.write( m[0] )
                fp.write( '\n' )
            else:
                shutil.rmtree(  m[0] )
                fp.write( m[0] )
                fp.write( '\n' )
        n += len( m[2] )
        print n
    print n
    fp.write('n: ')
    fp.write( str(n)  )
    fp.close()

path = '/data/news_data'
char = '2015_01_28'
delete_special_folders(path,char)
char = '2015_01_27'
delete_special_folders(path,char)






