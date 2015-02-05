#!/bin/sh
#scriptname:timer

function t {
    for i in 0 1 2 3 4 5 6 7 8 9;do
        echo -n "\t\t:\r"
        usleep 10
    done
}

print "Press CTRL+C OR CTRL+\ break!"

#while : ; do
#    print -n "Run.....星期三\r" ;t
#done



#!/bin/sh
abort()
{
    echo  "\033[m"
    exit
}

echo  "\033[2J"
echo  "\033[3;30H\c"
echo  "use CTRL-C to quit!"

while :
do
    echo  "\033[1;5m \033[8;26H\c"
    timestr='date "+%Y-%m-%d %H:%M:%S"'
    printf "    %s    " ""
    trap abort 2
done
