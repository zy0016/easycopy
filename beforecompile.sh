servername=`hostname`
echo "Check if sandbox deploy domino in "$servername

timestampfile="/tmp/timestamp"
if [ -f /tmp/auto.properties ];
then
	sudo rm -rf /tmp/auto.properties
fi

sudo /sbin/runuser -l jenkins -c 'aws s3 cp s3://aws-hcl-scn-opendom/Jenkins/auto.properties /tmp/'
DeployTheDomino1=`cat /tmp/auto.properties|grep DeployTheDomino=`
DeployTheDomino=`echo ${DeployTheDomino1##*=}`

trigger_od_publisher1=`cat /tmp/auto.properties|grep trigger_od_publisher=`
trigger_od_publisher=`echo ${trigger_od_publisher1##*=}`

trigger_od_populator1=`cat /tmp/auto.properties|grep trigger_od_populator=`
trigger_od_populator=`echo ${trigger_od_populator1##*=}`

trigger_od_prebuild1=`cat /tmp/auto.properties|grep trigger_od_prebuild=`
trigger_od_prebuild=`echo ${trigger_od_prebuild1##*=}`

trigger_od_automation1=`cat /tmp/auto.properties|grep trigger_od_automation=`
trigger_od_automation=`echo ${trigger_od_automation1##*=}`

echo "DeployTheDomino:"$DeployTheDomino
echo "trigger_od_prebuild:"$trigger_od_prebuild
echo "trigger_od_populator:"$trigger_od_populator
echo "trigger_od_publisher:"$trigger_od_publisher
echo "trigger_od_automation:"$trigger_od_automation
if [ $trigger_od_prebuild == "true" ];then
	sudo touch /tmp/prebuild
else
	sudo rm -rf /tmp/prebuild
fi
if [ $trigger_od_populator == "true" ];then
	sudo touch /tmp/populator
else
	sudo rm -rf /tmp/populator
fi
if [ $trigger_od_publisher == "true" ];then
	sudo touch /tmp/publisher
else
	sudo rm -rf /tmp/publisher
fi
if [ $trigger_od_automation == "true" ];then
	sudo touch /tmp/automation
else
	sudo rm -rf /tmp/automation
fi
