i=1
while  (($i<100))
do 
	#echo i is $i
	scrapy crawl baiduguonei
	#rm log_my_svn
	echo "update finished."
    rm './log'
	sleep  120;
done



rm log
echo "delete log finish."
