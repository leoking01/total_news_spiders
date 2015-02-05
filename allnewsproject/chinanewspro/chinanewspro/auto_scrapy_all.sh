#!/bin/sh
# coding: utf8

##scrapy 对话(仅仅当前的)
logfile="log"
##标准输出内容(仅仅当前的)
controlfile='log_scrapy_spider.txt'
##丢弃新闻内容(仅仅当前的)
diuqi='diuqi_xinwen_mark.txt'
##运行时间信息记录(累积)
runtime_mark_file='runtime_remark.txt'

logs_dir='./logs'
##i=1
##while  (($i<100))
while :
#i=1
##while (($i<2))
do 
    ##i=$i+1
    ##开始时间
    echo '==========    start     =========='
    starttime_s=`date '+%Y-%m-%d %H:%M:%S'`
    echo '运行开始时刻: ' >>$runtime_mark_file
    echo $starttime_s>>$runtime_mark_file
    starttime=`date '+%S'`


    ##运行
    scrapy crawl all_news  ####
	echo "process \"all_news_scrapy\"  has finished."


    ##结束时间
    endtime=`date '+%S'`
    endtime_s=`date '+%Y-%m-%d %H:%M:%S'`
    echo '运行结束时刻: ' >>$runtime_mark_file
    echo $endtime_s>>$runtime_mark_file


    ##作差
    runtime=$(($endtime-$starttime))
    runtime=`echo "sclae=5;$runtime/60"|bc`
    echo 'runtime(minute):' $runtime >>$runtime_mark_file
    echo ''>>$runtime_mark_file
    echo ''>>$runtime_mark_file


    ##logs处理
    #rm $logfile $controlfile $diuqi
    ##移动到logs文件夹，供分析查看。
    newfile=`date '+%Y_%m_%d_%H_%M_%S'`

    controlfile_s=$newfile$controlfile'.txt'
    logfile_s=$newfile$logfile'.txt'
    diuqi_s=$newfile$diuqi'.txt'
    runtime_mark_file_s=$newfile$runtime_mark_file'.txt'
    mv $controlfile  $controlfile_s
    mv $logfile   $logfile_s
    mv $diuqi  $diuqi_s
    mv $runtime_mark_file  $runtime_mark_file_s

    mv $controlfile_s  $logfile_s  $diuqi_s   $runtime_mark_file_s  $logs_dir
    echo "move file " $logfile $controlfile $diuqi $runtime_mark_file 'to dir' $logs_dir " success."

    echo '==========  finished    =========='
    echo ''

    ##延长间隔时间为三个小时.
    ##6个小时
    ##这是因为单次运行时间超过了一个小时.
    sleep  18000 ;
done



