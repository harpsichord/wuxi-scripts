#!/bin/bash
#Author: Wu Xi
#Mail Address: xi_wu@dell.com
#Date: 2016/1/13
#Purpose: Update BIOS/iDRAC settings

if [ $UID != 0 ]
then
echo 'You must be root to execute this script!'
exit 1
fi

if [ $# != 1 ]
then
echo 'You need to specify the ip list file'
exit 2
fi

ipList=$1
#sf='./settings'
cmd='/opt/dell/srvadmin/sbin/racadm -r'
ops='-u root -p calvin'
#numa_cmd='BIOS.MemSettings.NodeInterleave Enabled'
trap_addr='iDRAC.SNMP.Alert.DestAddr 192.168.1.100'

if [ ! -f $ipList ]
then
echo 'The file you specified is not exist'
exit 1
fi

while read iDRAC_ip
do
#Do stuff right here
#echo "$cmd $iDRAC_ip $ops getsysinfo"
#while read setting
#do
$cmd $iDRAC_ip $ops set "$trap_addr"
#done < $sf
#$cmd $iDRAC_ip $ops jobqueue create Bios.Setup.1-1
#Settings section done
done < $ipList
