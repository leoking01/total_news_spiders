myfile="./log"
i=1
while  (($i<100))
do 
#echo i is $i
    scrapy crawl pro  ####各省新闻抓取
    ####scrapy crawl s_yaowen  ####腾讯新闻中心  要闻   由于含有国际新闻。丢弃.
    ##last one
    ##################scrapy crawl sur   ####腾讯网首页  要闻   由于含有国际新闻。丢弃
    #scrapy crawl qq   
	#rm log_my_svn
	echo "update finished."
    #if [ -f "$myfile" ]  then
    #    rm "$myfile"
    #    echo "rm finish."
    #fi
    rm $myfile
    echo "rm log success."
	sleep  300;
done



