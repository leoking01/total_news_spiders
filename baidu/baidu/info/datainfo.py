#!/usr/bin/python
#! coding: utf-8
import os

#print '='*105
print '*'*120
print '*'*52,' file   count ',52*'*'
print '*'*120

print "自12月30日开始，当日数据不再与之前数据有重复."##.encode('utf-8')
##os.echo("自12月30日开始，当日数据不再有重复.".encode('utf-8'))

dirs_base='/data/news_data/'
dirs_main=os.listdir(dirs_base)
print 'director base: ',dirs_base
print 'directors list: '
for d in dirs_main:
    print d

for d in dirs_main:
    dir_0='/data/news_data/'+d
    print '\n'
    print 'directory: ',dir_0
    print '%-80s' %('='*120)
    print '%-80s %10s' %('director','number')
    all_total_number=0
    all_dir_number = 0
    date_number_dict={}
    for dir_a in os.listdir(dir_0):
        dir_b=dir_0+'/'+dir_a
        all_dir_number += 1
        print '\t%-70s %10s' %( dir_b,len( os.listdir(dir_b) )  )
        for dir_c in os.listdir(dir_b):
            dir_d = dir_b+'/'+dir_c
            if os.path.isdir(dir_d):
                number = len( os.listdir(dir_d) )
                if number==0:
                    print '\t\t%-70s %10s %10s' %( dir_d,number,'scrapy_failure'  )
                elif number<10:
                    print '\t\t%-70s %10s %10s' %( dir_d,number,'too_small'  )
                else:
                    print '\t\t%-70s %10s' %( dir_d,number  )
                all_total_number += number
                if date_number_dict.has_key(dir_c):
                    date_number_dict[dir_c]+=number
                else:
                    date_number_dict[dir_c]=number
    print '-'*33
    print '%-20s %10s' %('all_dir_number  :',all_dir_number)
    print '%-20s %10s' %('all_total_number:',all_total_number)
    print 'date_number_dict: \n',date_number_dict


print '\n\n'


