#!/bin/sh
# coding: utf8


logfile="./log"
controlfile='./log.txt'
i=1
#python -c 'import datetime
#datetime.datetime.now()
#' > start
#starttime=`date '+%Y-%m-%d %H:%M:%S'`
#starttime=`date '+%H:%M:%S'`
starttime=`date '+%S'`
#while  (($i<100))
#while :
while (($i<4))
do 
    ##scrapy crawl all_news  ####
	echo "all_news_scrapy has finished."
    ##rm $logfile $controlfile
    echo "rm file " $logfile '  '  $controlfile " success."
    ##修改时间为两个小时
	sleep  2 ;
    i=$i+1
done

#endtime=`date '+%Y-%m-%d %H:%M:%S'`
#endtime=`date '+%H:%M:%S'`
endtime=`date '+%S'`
echo 'starttime : ' $starttime
echo 'endtime   : ' $endtime

##作差
runtime=$(($endtime-$starttime))
echo 'runtime:(second) '  $runtime

####除法
##暂时只能整除啊
echo 'runtime:(minute) ' 
fenmu=2.0
number3=`echo "sclae=6;  $runtime/$fenmu"| bc`
echo $number3

runtime_mark_file='runtime_mark_file.txt'
echo 'runtime(minute):' $runtime >>$runtime_mark_file
echo 'runtime(minute):' `echo "sclae=5;$runtime/6"|bc` >>$runtime_mark_file
echo "">>$runtime_mark_file

##
newfile=`date '+%Y_%m_%d_%H_%M_%S'`
echo $newfile

newfile='abc'$newfile'.txt'
echo $newfile

cp $runtime_mark_file   $newfile

