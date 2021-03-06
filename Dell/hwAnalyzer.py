#!/usr/local/bin/python3.5
#coding: utf-8
#Author: Wu Xi
#Date: 2016/12/15
#Purpose: Analyze HW inventory

#from tabulate import tabulate as T
import xml.etree.ElementTree as ET
import subprocess
import concurrent.futures
import time
import argparse
import glob

#Create parser
parser = argparse.ArgumentParser(description='TSR analyzer in parallel')

#Add arguments
parser.add_argument('-d','--logdir', dest='logdir', help='Specify directory contains TSR logs', required=True)
args = vars(parser.parse_args())

ld = args['logdir']
tsr_files = glob.glob("{0}/*.xml".format(ld))

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

#Fetch values from element
def getValue(instances, property):
    for i in instances:
        for p in property:
            p_xpath = './PROPERTY[@NAME="{0}"]'.format(p)
            v = i.find(p_xpath)
            print("{0}: {1}".format(p, v.find('VALUE').text))

#Define a function to get Version Strings from TSR log
def getVer(tsr_file_name):
    tree = ET.parse(tsr_file_name)
    root = tree.getroot()

    for k in ins_dict.keys():
        if k == 'DCIM_ControllerView':
            ins_xpath = './Component[@Classname="{0}"][@Key="RAID.Integrated.1-1"]'.format(k)
        else:
            ins_xpath = './Component[@Classname="{0}"]'.format(k)
        instances = root.findall(ins_xpath)
        print("------{0}'s value------".format(mapping_dict[k]))
        getValue(instances, ins_dict[k])
    return 0

#Main loop
def tsrAnalyzer():
    t = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers = 4) as executor:
             future_to_TSR = {executor.submit(getVer, tsr_file): tsr_file for tsr_file in tsr_files}
             for future in concurrent.futures.as_completed(future_to_TSR):
                 tsr = future_to_TSR[future]
    c_t = time.time()

if __name__ == "__main__":
    tsrAnalyzer()
