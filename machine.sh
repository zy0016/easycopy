#!/bin/sh

durationdays=$1
username=$2
if [ -z $durationdays ];then
	durationdays=1
fi
findfreeserver="false"
hostname=""
while read line
do
	hostname=`echo $line|awk '{print $1}'`
	status=`echo $line|awk '{print $2}'`
	starttime=`echo $line|awk '{print $3}'`
	endtime=`echo $line|awk '{print $4}'`
	echo "hostname:"$hostname" status:"$status" starttime:"$starttime" endtime:"$endtime
	if [ $status == "free" ];
	then
		findfreeserver="true"
		currentdate=`date +%Y%m%d%H%M`
		year=`echo ${currentdate:0:4}`
		month=`echo ${currentdate:4:2}`
		day=`echo ${currentdate:6:2}`
		currenttime=`echo ${currentdate:8:4}`
		echo $currentdate" "$year" "$month" "$day" "$currenttime
		leapyear="false"
		let a=year%4
		let b=year%100
		let c=year%400
		if [ "$a" -eq "0" ] && [ "$b" -ne "0" ];then
			leapyear="true"
		elif [ "$c" -eq "0" ];then
			leapyear="true"
		else
			leapyear="false"
		fi
		maxday=0
		if [ $month == "01" ] || [ $month == "03" ] || [ $month == "05" ] || [ $month == "07" ] || [ $month == "08" ] || [ $month == "10" ] || [ $month == "12" ];then
			maxday=31
		elif [ $month == "04" ] || [ $month == "06" ] || [ $month == "09" ] || [ $month == "11" ];then
			maxday=30
		elif [ $leapyear == "true" ];then
			maxday=29
		else
			maxday=28
		fi
		# echo "leapyear:"$leapyear" maxday:"$maxday
		let plusday=day+durationdays
		echo "plusday:"$plusday" maxday:"$maxday
		
		newline=""
		newyear=""
		newmonth=""
		newday=""
		
		sed -i "/$hostname/d" machinelist.ini
		if [ $plusday -lt $maxday ];then
			# newline=$hostname" used   "$currentdate" "$year$month$plusday$currenttime
			$hostname" used   "$currentdate" "$year$month$plusday$currenttime" "$username>>machinelist.ini
		elif [ $plusday -eq $maxday ];then
			# newline=$hostname" used   "$currentdate" "$year$month$plusday$currenttime
			$hostname" used   "$currentdate" "$year$month$plusday$currenttime" "$username>>machinelist.ini
		else
			let newday=plusday-maxday
			if [ $newday -lt 10 ];then
				newday="0"$newday
			fi
			echo "newday:"$newday
			if [ $month -eq 12 ];then
				echo "month is 12:"$month
				newmonth=1
				let newyear=$year+1
			else
				echo "month is :"$month
				let newmonthtmp=$month+1
				if [ $newmonthtmp -lt 10 ];then
					newmonth="0"$newmonthtmp
				else
					newmonth=$newmonthtmp
				fi
				newyear=$year
				echo "newyear:"$newyear" newmonth:"$newmonth" newday:"$newday
			fi
			# newline=$hostname" used "$currentdate" "$newyear$newmonth$newday$currenttime
			$hostname" used "$currentdate" "$newyear$newmonth$newday$currenttime" "$username >>machinelist.ini
		fi
		# echo $newline
		# sed -i "/$hostname/d" machinelist.ini
		# echo $newline" "$username >>machinelist.ini
		break
	else
		echo $hostname " status is used, skip it."
	fi
done<machinelist.ini
if [ $findfreeserver == "true" ];then
	echo "hostname="$hostname>freemachine.txt
else
	rm -rf freemachine.txt
fi
