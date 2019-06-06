#!/bin/sh

username=$1
findfreeserver="false"
hostname=""
while read line
do
	hostname=`echo $line|awk '{print $1}'`
	status=`echo $line|awk '{print $2}'`
	starttime=`echo $line|awk '{print $3}'`
	echo "hostname:"$hostname" status:"$status" starttime:"$starttime
	if [ $status == "free" ];
	then
		findfreeserver="true"
		currentdate=`date +%Y%m%d%H%M`
		newline=$hostname" used   "$currentdate" forever "$username
		echo $newline
		sed -i "/$hostname/d" machinelist.ini
		# echo $newline" "$username >>machinelist.ini
		echo $hostname" used   "$currentdate" forever "$username >>machinelist.ini
		break
	else
		echo $hostname " status isn't free, skip it."
	fi
done<machinelist.ini
if [ $findfreeserver == "true" ];then
	echo "hostname="$hostname>freemachine.txt
else
	rm -rf freemachine.txt
fi
