#!/usr/bin/env python
#Author: Wu Xi
#Date: 09/20/2019
#Purpose: Get BIOS settings from inside OS environment without OEM tools
#Requirement: msr-tools

import subprocess
import json
import os.path

SYSFS_TURBO_PATH='/sys/devices/system/cpu/intel_pstate/no_turbo'
SYSFS_NUMA_PATH='/sys/devices/system/node/online'
SYSFS_PSTATES_PATH='/sys/devices/system/cpu/intel_pstate/num_pstates'
SYSFS_CSTATES_PATH='/sys/devices/system/cpu/cpuidle/current_driver'

'''
Reference:
1. Intel® 64 and IA-32 Architectures Software Developer's Manual Combined Volumes 3A, 3B, 3C, and 3D- System Programming Guidd
e
2. Intel® 64 and IA-32 Architectures Software Developer's Manual Volume 4- Model-Specific Registerst
'''
t_mask='38:38'
p_mask='16:16'
MSR_IA32_MISC_ENABLE='0x1A0'

#config
#keys are specific settings of BIOS
#values contains 2 items:
#    [0] - type of the data source, F: file; C: command
#    [1] - criterion against which we decide if the the setting is Enabled

res_dict = {}

settings_dict = {
  "Turbo": {
    "C": ["/usr/sbin/rdmsr {0} -f {1}".format(MSR_IA32_MISC_ENABLE, t_mask), '== 0']
  },
  "NUMA": {
    "F": [SYSFS_NUMA_PATH, '== 0-1']
  },
  "C-states": {
#    "C": ["/usr/bin/cpupower -c 15 idle-info | grep -F 'No idle states' -q", '== 0']
    "F": [SYSFS_CSTATES_PATH, '!= none']
  },
  "P-states": {
#    "F": [SYSFS_PSTATES_PATH, '> 10']
    "C": ["/usr/sbin/rdmsr {0} -f {1}".format(MSR_IA32_MISC_ENABLE, p_mask), '== 1']
  },
  "HT": {
    "C": ["/usr/bin/lscpu | grep -F 'Thread(s) per core' | cut -d ':' -f 2 | tr -d ' '", '== 2']
  }
}

def compare(crit, data):
    op = crit.split()[0]
    val = crit.split()[1]
    if op == '==':
        return 0 if data == val else 1
    elif op == '>':
        return 0 if data > val else 1
    elif op == '!=':
        return 0 if data > val else 1
    else:
        return 1

#case-switch
def rdFile(setting, cmd, crit):
    if os.path.isfile(cmd):
        with open(cmd, 'r') as sys:
            data = sys.read().strip('\n')
        return compare(crit, data)
    else:
        return 1

def exCmd(setting, cmd, crit):
#    print(setting, cmd, crit)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    o, e = p.communicate()
    if p.returncode == 0:
        data = o.strip('\n')
        return compare(crit, data)
    else:
        return 1

def operationType(i):
    switcher={
            'F':rdFile,
            'C':exCmd,
#            2:lambda:'two'
            }
    func=switcher.get(i,lambda :'Invalid')
    return func

def getValue(i, c):
    s = i
    for k in c.keys():
        type = k
        cmd = c[k][0]
        crit = c[k][1]
    m = operationType(type)
    return m(s, cmd, crit)

if __name__ == "__main__":
    for k in settings_dict.keys():
        rc = getValue(k, settings_dict[k])
        res_dict[k] = rc
    '''
    0 - The setting is enabled
    1 - The setting is disabled
    '''
    print(json.dumps(res_dict, indent=4, sort_keys=True))
