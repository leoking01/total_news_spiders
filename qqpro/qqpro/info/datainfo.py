#!/usr/bin/python
import os
dirs=os.listdir('/data/news_data/qq_news/')
print 'director list: \n',dirs

for d in dirs:
    dire='/data/news_data/qq_news/'+d
    print 'The number of files in ', dire, ' is: ',len( os.listdir(dire) )
print 'finish.'


