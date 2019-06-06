echo "Prepare download jar files from aws s3"
pwd
programpath=`cat /tmp/path`
echo "programpath:"$programpath
sudo rm -rf $programpath/*.html
timestampfile="/tmp/timestamp"
prebuildfile="/tmp/prebuild"
if [ -f $timestampfile ];
then
	sudo rm -rf $timestampfile
fi
if [ -f $prebuildfile ];
then
	sudo rm -rf $prebuildfile
fi
if [ -f /tmp/filename.properties ];
then
	sudo rm -rf /tmp/*.properties
fi
sudo rm -rf $programpath/*.html

echo "download timestamp file"
sudo /sbin/runuser -l jenkins -c 'aws s3 cp s3://aws-hcl-scn-opendom/Jenkins/timestamp /tmp/timestamp'
timestamp=`cat /tmp/timestamp`
echo "timestamp:"$timestamp
cd /tmp/
sudo /sbin/runuser -l jenkins -c 'aws s3 cp s3://aws-hcl-scn-opendom/Jenkins/auto.properties /tmp/'
r1=`cat auto.properties|grep rootDir`
rootDir=`echo ${r1##*=}`
echo "rootDir:"$rootDir
trigger_od_publisher1=`cat /tmp/auto.properties|grep trigger_od_publisher=`
trigger_od_publisher=`echo ${trigger_od_publisher1##*=}`
trigger_od_populator1=`cat /tmp/auto.properties|grep trigger_od_populator=`
trigger_od_populator=`echo ${trigger_od_populator1##*=}`
RunAutomationProgram1=`cat /tmp/auto.properties|grep RunAutomationProgram=`
RunAutomationProgram=`echo ${RunAutomationProgram1##*=}`
DeployTheDomino1=`cat /tmp/auto.properties|grep DeployTheDomino=`
DeployTheDomino=`echo ${DeployTheDomino1##*=}`
triggerowner1=`cat /tmp/auto.properties|grep trigger_owner=`
triggerowner=`echo ${triggerowner1##*=}`
echo $triggerowner>/tmp/triggerowner

hostname1=`cat /tmp/auto.properties|grep hostname=`
hostname=`echo ${hostname1##*=}`
echo $hostname>/tmp/host

begintime1=`cat /tmp/auto.properties|grep begintime=`
begintime=`echo ${begintime1##*=}`

if [ -d $rootDir ];
then
	echo "Find the "$rootDir
else
	sudo mkdir -p $rootDir
fi

cleandir=$rootDir/logs
if [ -d $cleandir ];
then
	echo "Find the "$cleandir
else
	sudo mkdir -p $cleandir
fi
reportdir=$rootDir/reports
if [ -d $reportdir ];
then
	echo "Find the "$reportdir
else
	sudo mkdir -p $reportdir
fi

populatordir=$rootDir/populator
if [ -d $populatordir ];then
	echo "Find the "$populatordir
else
	sudo mkdir -p $populatordir
fi
publisherdir=$rootDir/publisher
if [ -d $publisherdir ];then
	echo "Find the "$publisherdir
else
	sudo mkdir -p $publisherdir
fi

sudo chmod 777 -R $rootDir

pwd

if [ $trigger_od_publisher == "true" ] || [ $trigger_od_populator == "true" ];then
	echo "Get latest jar from s3 od-automation-staging"
	sudo rm -rf *.jar
	sudo rm -rf *.so
	sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-automation-staging/s"$timestamp"/linux64/autopopulator-1.0.0.jar /tmp/"
	sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-automation-staging/s"$timestamp"/linux64/autopublisher-1.0.0.jar /tmp/"
	sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-automation-staging/s"$timestamp"/linux64/config.properties /tmp/"
	sudo mv autopopulator-1.0.0.jar $rootDir
	sudo mv autopublisher-1.0.0.jar $rootDir
	sudo mv config.properties $rootDir

	echo "Get latest so from s3 od-prebuild-staging"
	
	libext="libpubsubem.so"
	notefolder="/opt/ibm/domino/notes/10000000/linux/"
	sudo /sbin/runuser -l jenkins -c "aws s3 ls s3://aws-hcl-scn-opendom/od-prebuild-staging/>"$prebuildfile
	sudo sed -i 's/PRE//g' $prebuildfile
	sudo sed -i 's/\///g' $prebuildfile
	sudo sed -i 's/ //g' $prebuildfile
	latesttimestamp=`tail -n 1 $prebuildfile`
	echo "latesttimestamp:"$latesttimestamp
	sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-prebuild-staging/"$latesttimestamp"/linux64/"$libext" /tmp/"
	sudo cp -f /tmp/$libext $notefolder
	sudo chmod 755 $notefolder$libext

	pluginpath="/opt/ibm/domino/notes/latest/linux/osgi-dots/shared/eclipse/plugins"
	if [ $trigger_od_populator == "true" ];then
		echo "Get latest jar from s3 od-populator-staging"
		sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-populator-staging/s"$timestamp"/linux64/filename.properties /tmp/"
		populatorfilename=`cat /tmp/filename.properties`
		echo "populatorfilename:"$populatorfilename
		sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-populator-staging/s"$timestamp"/linux64/"$populatorfilename" /tmp/"
		sudo rm -rf $pluginpath/populator-*.jar
		sudo cp -f $populatorfilename $pluginpath"/"
		sudo chmod 755 $pluginpath/$populatorfilename
	fi
	if [ $trigger_od_publisher == "true" ];then
		echo "Get latest jar from s3 od-publisher-staging"
		sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/filename.properties /tmp/"
		
		publisherfilename=`cat /tmp/filename.properties`
		echo "publisherfilename:"$publisherfilename
		sudo rm -rf $pluginpath/publisher-*.jar
		sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/"$publisherfilename" /tmp/"
		ls -l /tmp/*.jar
		
		sudo cp -f /tmp/$publisherfilename $pluginpath"/"
		sudo chmod 755 $pluginpath/$publisherfilename
	fi
fi

if [ $DeployTheDomino == "true" ];then
	echo "prepare deploy domino and jar files"
	export JAVA_HOME=/opt/jdk1.8.0_191
	sudo /opt/clean.sh
	pubpath="s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/"
	poppath="s3://aws-hcl-scn-opendom/od-populator-staging/s"$timestamp"/linux64/"
	autpath="s3://aws-hcl-scn-opendom/od-automation-staging/s"$timestamp"/linux64/"
	sudo echo "{\"od_pop_fullurl\":\""$poppath"\",\"od_pub_fullurl\":\""$pubpath"\",\"od_auto_fullurl\":\""$autpath"\"}" > /home/jenkins/build.json
	cat /home/jenkins/build.json
	sudo chef-client -j /home/jenkins/build.json
	echo "sleep 60s"
	sleep 60
else
	echo "Don't deploy domino in "$servername
fi

echo "get dblist"
Databasepop=`cat $rootDir/config.properties|grep ^databases_pop=`
databases_pop=`echo ${Databasepop##*=}`
echo "databases_pop:"$databases_pop

Databasepub=`cat $rootDir/config.properties|grep ^databases_pub=`
databases_pub=`echo ${Databasepub##*=}`
echo "databases_pub:"$databases_pub

echo "Populator databases list:"$databases_pop>/tmp/dblist
echo "<br>Publisher databases list:"$databases_pub>>/tmp/dblist
cat /tmp/dblist

cd $rootDir
. /etc/profile
pwd
ls -l
testresult="true"
findreportfile="false"
allpopulatorpass="true"
allpublisherpass="true"
findreport="/tmp/findreportfile"
pubeventtalbe="PubEventTable.html"

echo "withoutreportfile">$findreport
if [ $RunAutomationProgram == "true" ];
then
	sudo rm -rf populatorreport/*.html
	sudo rm -rf publisherreport/*.html
	starttime1=`date +%Y-%m-%d/%H:%M`
	echo "Run test case on:"$starttime1
	currenttimestamp=`date +%Y%m%d%H%M`"00"
	
	sudo /sbin/runuser -l jenkins -c 'aws s3 cp s3://aws-hcl-scn-opendom/Jenkins/run.sh /tmp/'
	cd /tmp/
	runuser - notes /tmp/run.sh $rootDir

	if [ -f /tmp/automationover ];then
		echo "find the automationover"
		sudo rm -rf /tmp/automationover
	else
		echo "can't find the automationover,maybe the program is killed."
		return 1
	fi
	
    endtime1=`date +%Y-%m-%d/%H:%M`
	echo "Test end on:"$endtime1
    
	cd $rootDir
	echo "check report for populatorreport"
    ls -l populatorreport/*.html|awk '{print $9}'>r.txt
	sed -i 's/populatorreport\///g' r.txt
	while read line
	do
		echo "line:"$line
		color=`cat populatorreport/$line|grep "#FF1010"`
		if [ -z $color ];then
			echo "not find #FF1010 for "$line
		else
			allpopulatorpass="false"
		fi
		findreportfile="true"
		echo "copy the populatorreport/"$line" to "$programpath
		sudo cp populatorreport/$line $programpath
	done<r.txt
	ls $programpath>/tmp/pophtmllist
	
	echo "check report for publisherreport"
	ls -l publisherreport/*.html|awk '{print $9}'>r.txt
	sed -i 's/publisherreport\///g' r.txt
	while read line
	do
		echo "line:"$line
		color=`cat publisherreport/$line|grep "#FF1010"`
		if [ -z $color ];then
			echo "not find #FF1010 for "$line
		else
			allpublisherpass="false"
		fi
		findreportfile="true"
		if [ $line == $pubeventtalbe ];then
			echo "Don't copy the "$pubeventtalbe
		else
			echo "copy the publisherreport/"$line" to "$programpath
			sudo cp publisherreport/$line $programpath
		fi
		
	done<r.txt
	if [ -f publisherreport/$pubeventtalbe ];then
		sudo cp publisherreport/$pubeventtalbe /tmp/
	fi
	
	ls $programpath>/tmp/pubhtmllist
	
	if [ -f d.txt ];then
		sudo rm -rf d.txt
	fi
	if [ $findreportfile == "true" ];then
		echo "findreportfile">$findreport
	else
		echo "withoutreportfile">$findreport
	fi
	
	populatorresultfailfile="/tmp/popautoresultfalse"
	publisherresultfailfile="/tmp/pubautoresultfalse"
	if [ $allpopulatorpass == "false" ];then
		echo "Find populator failure case."
		sudo touch $populatorresultfailfile
	else
		echo "All populator test case pass."
		sudo rm -rf $populatorresultfailfile
	fi
	if [ $allpublisherpass == "false" ];then
		echo "Find publisher failure case."
		sudo touch $publisherresultfailfile
	else
		echo "All populator test case pass."
		sudo rm -rf $publisherresultfailfile
	fi
	
    sudo rm -rf r.txt
fi

if [ $allpopulatorpass == "true" ];then
	echo "all populator pass"
	if [ $allpublisherpass == "true" ];then
		echo "all publisher pass"
		testresult="true"
	else
		echo "set testresult is false"
		testresult="false"
	fi
else
	echo "set testresult is false"
	testresult="false"
fi

if [ $testresult == "true" ];then
	if [ $trigger_od_publisher == "true" ] || [ $trigger_od_populator == "true" ];then
		echo "copy files from staging to official folder."
		if [ -f /tmp/populator ];
		then
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-populator-staging/s"$timestamp"/linux64/filename.properties /tmp/filename.properties"
			populatorfilename=`cat /tmp/filename.properties`
			echo "populatorfilename:"$populatorfilename
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-populator-staging/s"$timestamp"/linux64/"$populatorfilename" s3://aws-hcl-scn-opendom/od-populator/p"$timestamp"/linux64/"
		fi
		if [ -f /tmp/publisher ];
		then
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/libpubsubem.so s3://aws-hcl-scn-opendom/od-publisher/p"$timestamp"/linux64/"
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/libdomjni.so s3://aws-hcl-scn-opendom/od-publisher/p"$timestamp"/linux64/"
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/filename.properties /tmp/filename.properties"
			publisherfilename=`cat /tmp/filename.properties`
			echo "publisherfilename:"$publisherfilename
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/"$publisherfilename" s3://aws-hcl-scn-opendom/od-publisher/p"$timestamp"/linux64/"
			
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/amqpluginfilename.properties /tmp/amqpluginfilename.properties"
			publisherpluginfilename=`cat /tmp/amqpluginfilename.properties`
			echo "publisherpluginfilename:"$publisherpluginfilename
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/"$publisherpluginfilename" s3://aws-hcl-scn-opendom/od-publisher/p"$timestamp"/linux64/"
			
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/activemq-all-5.14.5.jar s3://aws-hcl-scn-opendom/od-publisher/p"$timestamp"/linux64/"
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/commons-pool2-2.6.0.jar s3://aws-hcl-scn-opendom/od-publisher/p"$timestamp"/linux64/"
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/gson-2.8.5.jar s3://aws-hcl-scn-opendom/od-publisher/p"$timestamp"/linux64/"
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/jasypt-1.9.2.jar s3://aws-hcl-scn-opendom/od-publisher/p"$timestamp"/linux64/"
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-publisher-staging/s"$timestamp"/linux64/log4j_pubsub.properties s3://aws-hcl-scn-opendom/od-publisher/p"$timestamp"/linux64/"
		fi
		if [ -f /tmp/automation ];
		then
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-automation-staging/s"$timestamp"/linux64/autopublisher-1.0.0.jar s3://aws-hcl-scn-opendom/od-automation/p"$timestamp"/linux64/"
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-automation-staging/s"$timestamp"/linux64/autopopulator-1.0.0.jar s3://aws-hcl-scn-opendom/od-automation/p"$timestamp"/linux64/"
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-automation-staging/s"$timestamp"/linux64/SecurityPluginTest-1.0.jar s3://aws-hcl-scn-opendom/od-automation/p"$timestamp"/linux64/"
			sudo /sbin/runuser -l jenkins -c "aws s3 cp s3://aws-hcl-scn-opendom/od-automation-staging/s"$timestamp"/linux64/config.properties s3://aws-hcl-scn-opendom/od-automation/p"$timestamp"/linux64/"
		fi
	fi
fi

echo "begin time:"$begintime
endtime=`date +%s`
echo "end time:"$endtime
minute=0
let interval=endtime-begintime
let minute=interval/60
echo "interval:"$interval
echo $minute>/tmp/interval

sudo rm -rf $prebuildfile
sudo rm -rf $timestampfile
sudo rm -rf /tmp/*.properties
sudo rm -rf /tmp/run.sh
sudo rm -rf $rootDir/*.sh
sudo rm -rf /tmp/*.xml
sudo rm -rf /tmp/*.so

