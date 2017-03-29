#!/bin/bash
#Date: 20170314
#Purpose: Collect TSR log from iDRAC

function usage()
{
  echo "Usage: ./wuxi-tsr_collector.sh -i idrac_ip"
  echo ""
}

function banner()
{
  title='Collect TSR log from remote iDRAC'
  ver="Wu Xi - 1.0(20170314)"
  printf "%40s\n" "$title"
  printf "%40s\n" "$ver"
  printf "%40s\n" "------"
}

if [ $# -ne 2 ]
then
  echo "You need to specify iDRAC ip"
  usage
exit 1
fi

#Parse options
set -- $(getopt "i:" "$@")
while [ ! -z "$1" ]
do
  case "$1" in
    -i) RAC_IP=$2;;
  esac
  shift
done

# Constant part of racamd command line #
RACADM_CMD='/opt/dell/srvadmin/bin/idracadm7 -r '
RACADM_FLAGS=' -u root -p calvin --nocertwarn'
RACADM_COLLECT=' techsupreport collect -t SysInfo,TTYLog'
RACADM_JOBVIEW=' jobqueue view -i '
RACADM_EXPORT=' techsupreport export -f '
RACADM_VER='getversion -f idrac'
RACADM_SVCTG='getsvctag'
RACADM_SEL='getsel -E | tr -d '
''
#RACADM_RACLOG='getraclog | tr -d '
''
RACADM_RACLOG='lclog export -f /tmp/lclog.xml'

#Set exported filename of TSR log
TSR_FN="${RAC_IP}-tsrlog.zip"
RLC_FN="${RAC_IP}-RawLC.tar.gz"

########################################
# Various status of the Job            #
########################################
#Job ID
JID=''
#Status of the Job
JS=''
#Completeness of the Job
JP=''
#iDRAC FW version
ifw=''
#System Service Tag
st=''
#2.30.30.30 FW constant
sfw='2303030'

#banner
########################################
# Get iDRAC FW version                 #
########################################
function getVer()
{
    x=$($RACADM_CMD $RAC_IP $RACADM_FLAGS $RACADM_VER | tr -d '^M .')
    set -- $(echo $x | tr -t '=' ' ')
    ifw=$2
}

########################################
# Get Service Tag                      #
########################################
function getSvcTag()
{
    x=$($RACADM_CMD $RAC_IP $RACADM_FLAGS $RACADM_SVCTG | tr -d '
 .')
    st=$x
}

########################################
# Get status of TSR log collection     #
# Still, non-printable chars are tricky#
########################################
function getJobStatus()
{
  T=$($RACADM_CMD $RAC_IP $RACADM_FLAGS $RACADM_JOBVIEW $JID | tr '\r' ',')
  JS=$(echo $T | gawk 'BEGIN { RS=","; FS="=" } /Status/ {print $2}')
  JP=$(echo $T | gawk 'BEGIN { RS=","; FS="=" } /Percent Complete/ {print $2}')
  printf "Job Status:%8s\n" "${JS}"
  printf "Job Completeness:%2s\n" "${JP}"
}

########################################
# Main logic                           #
########################################
getSvcTag
getVer

echo -e "Service Tag:\t$st"

if [ "$ifw" -gt $sfw ]
then
echo "New FW, proceed to collect TSR log along with TTY log"
########################################
# Initiate TSR log collection          #
# Output from this command contains    #
# several non-printable chars          #
# It's pretty tricky                   #
########################################
JID=$($RACADM_CMD $RAC_IP $RACADM_FLAGS $RACADM_COLLECT | tr -dc '[[:print:]]' | grep -ioE 'JID_[[:digit:]]{12}')

#Sleep a while
echo 'Let the job run for a while...'
sleep 10

getJobStatus
while [ "$JP" != '[100]' ]
do
  echo 'Job is still running...'
  sleep 10
  getJobStatus
done

if [ "$JS" == 'Completed with Errors' ]
then
  echo 'Job failed, abort!'
  exit 1
fi

########################################
# Export TSR log collection            #
########################################
echo "Saving TSR log in current directory...[$TSR_FN]"
sleep 60
$RACADM_CMD $RAC_IP $RACADM_FLAGS $RACADM_EXPORT $TSR_FN
else
echo "Old FW, SEL raw and raclog will be collected instead of TSR log"
$RACADM_CMD $RAC_IP $RACADM_FLAGS $RACADM_SEL > /tmp/sel.raw 2>&1
$RACADM_CMD $RAC_IP $RACADM_FLAGS $RACADM_RACLOG
tar cvfz $RLC_FN /tmp/sel.raw /tmp/lclog.xml
fi
