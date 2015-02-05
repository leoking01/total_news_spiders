#!/usr/bin/python
#  -*- coding:utf8 -*-


id = 0

class cat(  object ):
    def __init__(self):
        name = ''
        code = ''
        pass 
        ##__firstname = '123'

    name = ''
    __firstname = 'ghj'##object

    def show_f_name(self):
        ##print '__firstname : ', __firstname
        print 'show_f_name : name =  ', self.name


##########################################

a = cat(  )
cc = cat(  )

cc.name = 'wajue'
print 'cc.name :', cc.name

cc.show_f_name()





