#!/usr/bin/bash
#Author: Wu Xi
#Date: 09/19/2019
#Purpose: Get firmware, driver versions of all key hardware components
#
#Version Categories:
#--CPU: microcode
#--BIOS: firmware version
#--BMC: firmware version
#--RAID/HBA controller: driver/firmware
#    |+HDD/SSD/NVMe: firmware
#--NIC: driver/firmware
#--GPU: driver/firmware

function usage {
   echo >&2 "USAGE: satVersions.sh -d sos_log_dir"
   exit
}

if [ $# != 2 ]
then
    usage
    exit 1
fi

#Variables declaration
sos_log_dir=''
lscpu_f='/sos_commands/processor/lscpu'
mcinfo_f='/sos_commands/ipmitool/ipmitool_mc_info'
mc_sys_path='/sys/devices/system/cpu/cpu0/microcode/version'
bv_sys_path='/sys/devices/virtual/dmi/id/bios_version'
nic_sys_path='/sos_commands/networking/ethtool_-i_e*'
nic_list=''

while getopts d:h opt
do
    case $opt in
    d)  sos_log_dir=$OPTARG ;;
    h|?)  usage ;;
    esac
done

#main
function getNicInfo()
{
read -d '' gawk_str << 'EOF'
BEGIN {
  drv_name = 0;
  drv_ver = 0;
  fw_ver = 0;
}
{
n = index($i, ":");          # search for =
# if you know precisely what variable names you expect to get, you can assign to them here:
if ( $0 ~ /^driver/ ) {
  vars[substr($i, 1, n - 1)] = substr($i, n + 1)
  drv_name = vars["driver"];
}
if ( $0 ~ /^version/ ) {
  vars[substr($i, 1, n - 1)] = substr($i, n + 1)
  drv_ver = vars["version"];
}
if ( $0 ~ /^firmware-version/ ) {
  vars[substr($i, 1, n - 1)] = substr($i, n + 1)
  fw_ver = vars["firmware-version"];
}
}
END {
  print drv_name drv_ver fw_ver;
}
EOF
gawk "$gawk_str" $1
}

#CPU microcode
cpu_mc_ver=$(cat ${sos_log_dir}${mc_sys_path})
cpu_model=$(gawk -F ':' '/^Model name:/ {sub(/^[ \t]*/, "", $NF); print $NF; exit}' ${sos_log_dir}${lscpu_f})
printf "%s:%s\n" "${cpu_model}" "${cpu_mc_ver}"

#BIOS
bios_version=$(cat ${bv_sys_path})
printf "BIOS:%s\n" "${bios_version}"

#BMC
bmc_ver=$(gawk -F ':' '/^Firmware Revision/ {sub(/^[ \t]*/, "", $NF); print $NF; exit}' ${sos_log_dir}${mcinfo_f})
printf "BMC:%s\n" "${bmc_ver}"

#Storage
#Invoke satBlockInfo.py

#NIC
for i in $(ls -1 ${sos_log_dir}${nic_sys_path})
do
    nic="${i##*_}"
    nic_ver_info=$(getNicInfo $i)
    printf "%s:%s\n" "${nic}" "${nic_ver_info}"
done
