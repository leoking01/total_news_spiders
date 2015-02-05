i=1
while  (($i<100))
do 
	#echo i is $i
	scrapy crawl sina
	#rm log_my_svn
	echo "update finished."
    rm './log'
	sleep  180;
done



rm log
echo "delete log finish."
