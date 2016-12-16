#!/usr/local/bin/python3.5

import xml.etree.ElementTree as ET

hwi = 'hwinventory/hwinventory.xml'

tree = ET.parse(hwi)
root = tree.getroot()

#Value list
ctrl_list = ['ProductName', 'ControllerFirmwareVersion']
sys_list = ['ChassisServiceTag', 'BIOSVersionString', 'LifecycleControllerVersion']
nic_list = ['ProductName', 'FamilyVersion']
cpu_list = ['Model', 'CurrentClockSpeed']
mem_list = ['Manufacturer', 'Size']

#Component list
ins_dict = {'DCIM_SystemView': sys_list,
            'DCIM_ControllerView': ctrl_list,
            'DCIM_NICView': nic_list,
            'DCIM_CPUView': cpu_list,
            'DCIM_MemoryView': mem_list,
#            'DCIM_PhysicalDiskView': pd_list
            }

mapping_dict = {'DCIM_SystemView': 'System Info',
                'DCIM_ControllerView': 'PERC Controller Info',
                'DCIM_NICView': 'Network Interfaces Info',
                'DCIM_PhysicalDiskView': 'Physical Disks Info',
                'DCIM_CPUView': 'CPU Info',
                'DCIM_MemoryView': 'Memory Info',
                }

def getValue(instances, property):
    for i in instances:
        for p in property:
            p_xpath = './PROPERTY[@NAME="{0}"]'.format(p)
            v = i.find(p_xpath)
            print("{0}: {1}".format(p, v.find('VALUE').text))

for k in ins_dict.keys():
    if k == 'DCIM_ControllerView':
        ins_xpath = './Component[@Classname="{0}"][@Key="RAID.Integrated.1-1"]'.format(k)
    else:
        ins_xpath = './Component[@Classname="{0}"]'.format(k)
    instances = root.findall(ins_xpath)
    print("------{0}'s value------".format(mapping_dict[k]))
    getValue(instances, ins_dict[k])
