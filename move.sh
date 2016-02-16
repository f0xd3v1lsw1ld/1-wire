#!/bin/sh

#us this script to rename temperature logfile of yesterday each day at 0:00
# crontab -e
# minute(0-59)
#    hour(0-23)
#      day of the month(1-31)
#        month of the year(1-12)
#          day of the week(0-6, starts with 0=Sunday)
# 00 0 * * * /home/pi/1-wire/move.sh /home/pi/1-wire rpi_temperature.csv>>/dev/null


#store date of yesterday i.e. 20150325
DATE=$(date --date yesterday +%Y%m%d )

# control if there are two parameter, this must be the directory and the filename
# if there are no parameter, print usage an exit
if [ $# != 2 ]; then
     echo "usage: $0 directory filename"
     exit
fi

#control if the first parameter is an existing directory
# if not print an error and exit
if [ ! -d $1 ]; then
    echo "No such directory $1"
    exit
fi


#go into the directory
cd $1

#control if the second parameter is an existing file
# if not print an error and exit
if [ ! -f $2 ]; then
    echo "No such file $2"
    exit
fi

# rename given file(first paramter) to current date
mv $1"/"$2 $1"/"$DATE"_"$2

# print result
echo $1"/"$2 "renamed to " $1"/"$DATE"_"$2
