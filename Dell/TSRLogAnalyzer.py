#!/usr/local/bin/python3.5
#coding: utf-8
#Author: Wu Xi
#Purpose: TSR log analyzer

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
#tsr_log = 'tsr_extracted/tsr/sysinfo/inventory/sysinfo_DCIM_View.xml'

#Define a function to get Version Strings from TSR log
def getVer(tsr_file_name):
    tree = ET.parse(tsr_file_name)
    root = tree.getroot()

    for item in root.iter('PROPERTY'):
        if item.attrib['NAME'] == 'ChassisServiceTag':
            ST = item.find('VALUE').text
        if item.attrib['NAME'] == 'BIOSVersionString':
            BIOSVer = item.find('VALUE').text
        if item.attrib['NAME'] == 'LifecycleControllerVersion':
            idracVer = item.find('VALUE').text
        if item.attrib['NAME'] == 'ControllerFirmwareVersion':
            if item.find('VALUE').text is not None:
                PercVer = item.find('VALUE').text

    print("{0}: {1}, {2}, {3}".format(ST, BIOSVer, idracVer, PercVer))
    return 0

#Main loop
if __name__ == "__main__":
    t = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers = 4) as executor:
             future_to_TSR = {executor.submit(getVer, tsr_file): tsr_file for tsr_file in tsr_files}
             for future in concurrent.futures.as_completed(future_to_TSR):
                 tsr = future_to_TSR[future]
#                 res = future.result()
#                 if res == 0:
#                     print("{}:\tGood".format(tsr))
#                 else:
#                     print("{}:\tFailed".format(tsr))
    c_t = time.time()
    print("It took {0} seconds to analyze {1} logs".format((c_t - t), len(tsr_files)))
