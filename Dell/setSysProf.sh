#!/bin/bash
#Purpose: Set system profile to PerfOptimzed(Max Performance)
#Date: 20170811

in_f=$1

if [ ! -f $in_f ]
then
echo "$in_f does not exist, exit"
exit 2
fi

#Constants declaration
RAC='/opt/dell/srvadmin/bin/idracadm7 -r' 

for entry in $(cat $in_f)
do
set -- $(echo $entry | tr -t "," " ")
RAC_OPTS="-u $2 -p $3 --nocertwarn "
$RAC $1 $RAC_OPTS set bios.sysprofilesettings.SysProfile PerfOptimized
$RAC $1 $RAC_OPTS jobqueue delete --all > /dev/null 2>&1
$RAC $1 $RAC_OPTS jobqueue create Bios.Setup.1-1
done
