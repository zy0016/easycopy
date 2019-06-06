#!/bin/sh
source ~/.bash_profile

#set project name
project=$1
jartype=$2
s3datetime=$3
echo "start to build project $project"
if [ -z $1 ]; then
	echo "must set a project name $0 'projectname'"
	exit -1
fi

basedir=$(dirname "$0")
cd $basedir
echo start on directory `pwd`
#install dependendency jars

awscmd=aws
s3folderbase=aws-hcl-scn-opendom
s3foldercommns=rdz-common
s3projectfolder=""
if [ $jartype == "staging" ]; then
	s3projectfolder=$project"-"$jartype"/s"$s3datetime"/linux64"
else
	s3projectfolder=$project"/p"$s3datetime"/linux64"
fi
#commonfolder=commons
#if [ -d "$commonfolder" ]
#then 
#	echo "enter folder"
#else
	# mkdir $commonfolder
#fi

if  ! type "$awscmd" > /dev/null; then
	echo "$awscmd not exists, install by this guide https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-linux.html#awscli-install-linux-path "
	exit -1;
	else
		awsauth=`aws s3 ls $s3folderbase|grep $s3foldercommns`
		if [ -z "$awsauth" ]
		then
			echo "aws issue, should check on aws configure, all credentials should be set"
			exit -1;
		fi
		
fi

# cd $commonfolder
# currentPath=`pwd`
# echo "downlaod jars to $currentPath"
# aws s3 cp s3://$s3folderbase/$s3foldercommns/ . --recursive
# for file in *.bat; do
	  # mv "$file" "$(basename "$file" .bat).sh"
# done
# sed -i -- 's/bat/sh/g' install_jar.sh
# chmod 755 *.sh

# for file in *.sh;do
	# if [ $file = "install_jar.sh" ]
	# then
		# continue
	# else
		# ./$file
	# fi
# done


# echo "install all jars to mvn repository"

# cd ..
currentPath=`pwd`
# docker sections
echo "check file $currentPath/docker.config"
if [ -f "$currentPath/docker.config" ]
then
	echo "read docker.config file"
	. $currentPath/docker.config
else
   echo "docker.config not found"
   currentPath=`pwd`
   echo "current directory is $currentPath"
   exit -1
fi
imagename=$project
bimage=`sudo docker image ls $imagename|awk 'NR=2'`

#clear docker images
if [ -z "$bimage" ]
then
	echo "no image found for $imagename"
else
	echo "find images,delete $imagename"
	sudo docker image rm $imagename
fi


cp -rf "Dockerfile.template" "Dockerfile"
dockerfilename="Dockerfile"
echo "RUN mkdir /opt/$project" >> $dockerfilename
cd ../
currentPath=`pwd`
echo "current path:$currentPath"

sudo mkdir -p ./build-rz-$project/rz.$project/target/
sudo rm -rf ./build-rz-$project/rz.$project/target/*.jar
sudo rm -rf ./build-rz-$project/rz.$project/target/*.so
sudo rm -rf ./build-rz-$project/rz.$project/target/*.properties
sudo cp /tmp/*.jar ./build-rz-$project/rz.$project/target/

tp1=`ls ./build-rz-$project/rz.$project/target/*.jar`
tpn=`ls ./build-rz-$project/rz.$project/target/*.jar|wc -l`
cd dockertask
currentPath=`pwd`
echo "current path:$currentPath"
echo "COPY $tp1 /opt/$project" >> $dockerfilename
echo "RUN mkdir /opt/$project/lib" >> $dockerfilename
echo "COPY  ./build-rz-$project/rz.$project/target/dependency-jars/ /opt/$project/lib/" >> $dockerfilename

#build docker
cd ../
dockerCtx=`pwd`
echo "docker context $dockerCtx"
sudo docker build --rm -t $imagename . -f ./dockertask/Dockerfile
sudo docker run --rm $imagename java -version
echo "-----------show jars in $project image-----------------"
#sudo docker run --rm $imagename ls /opt/verse/
sudo docker run --rm $imagename ls /opt/$project/
#copy jar to s3
currentPath=`pwd`
echo "-------------copy file to s3 buckets-----------------"
echo "cp $currentPath/$tp1 s3://$s3folderbase/$s3projectfolder/"

if [ "$tpn" -gt 1 ]
then
	tp2=`ls ./build-rz-$project/rz.$project/target/*.jar`
	for loop in $tp2
	do
		aws s3 cp $currentPath/$loop s3://$s3folderbase/$s3projectfolder/
	done
else
	aws s3 cp $currentPath/$tp1 s3://$s3folderbase/$s3projectfolder/ 
fi

echo "copy the propertiese files"
ls -l /tmp/*.properties
if [ $? -eq 0 ]
then
	sudo cp /tmp/*.properties ./build-rz-$project/rz.$project/target/
	tpp=`ls ./build-rz-$project/rz.$project/target/*.properties`
	tpn2=`ls ./build-rz-$project/rz.$project/target/*.properties|wc -l`
	if [ "$tpn2" -gt 1 ]
	then
		for loop in $tpp
		do
			aws s3 cp $currentPath/$loop s3://$s3folderbase/$s3projectfolder/
		done
	else
		aws s3 cp $currentPath/$tpp s3://$s3folderbase/$s3projectfolder/ 
	fi
fi

echo "copy the so files"
ls -l /tmp/*.so
if [ $? -eq 0 ]
then
	sudo cp /tmp/*.so ./build-rz-$project/rz.$project/target/
	tpso=`ls ./build-rz-$project/rz.$project/target/*.so`
	tpsonum=`ls ./build-rz-$project/rz.$project/target/*.so|wc -l`
	if [ "$tpsonum" -gt 1 ]
	then
		for loop in $tpso
		do
			aws s3 cp $currentPath/$loop s3://$s3folderbase/$s3projectfolder/
		done
	else
		aws s3 cp $currentPath/$tpso s3://$s3folderbase/$s3projectfolder/ 
	fi
fi
