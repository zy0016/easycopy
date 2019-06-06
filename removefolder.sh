#!/bin/sh

echo "remove folder"

filename=$1
remainitem=$2
projectname=$3
echo "filename:"$filename
echo "remainitem:"$remainitem
if [ $remainitem == "RemainAll" ];then
	echo "Don't remove build items for"
	return 0
fi

s3mainfolder="s3://aws-hcl-scn-opendom/"
linecount=`awk 'END{print NR}' $filename`
echo "linecount:"$linecount
i=0
if [ $linecount -le $remainitem ];then
	echo "Don't remove build items"
else
	let removeitem=$linecount-$remainitem
	echo "need remove:"$removeitem
	while read line
	do
		if [ $i -lt $removeitem ];then
			nospace=`echo $line| sed -e 's/^[ \t]*//g'`
			subfoldername=`echo ${nospace##* }`
			echo "remove the >>>>>>>>>>>>>>>>"$subfoldername" for "$projectname
			sudo /sbin/runuser -l jenkins -c "aws s3 rm "$s3mainfolder$projectname"/"$subfoldername" --recursive"
			sudo sleep 1
			sudo /sbin/runuser -l jenkins -c "aws s3 rm "$s3mainfolder$projectname"/"$subfoldername
			let i=$i+1
		else
			echo "break"
			break
		fi
	done<$filename
fi

	
