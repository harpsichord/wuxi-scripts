#!/usr/local/bin/python3.5
#coding: utf-8
#Author: Wu Xi <xi_wu@dell.com>
#Purpose: LifeCycle(contained in TSR log) log analyzer

#from tabulate import tabulate as T
import xml.etree.ElementTree as ET
import argparse
import datetime
from tabulate import tabulate as T

#Create parser
parser = argparse.ArgumentParser(description='LifeCycle events analyzer')

#Add arguments
parser.add_argument('-f','--logfile', dest='logfile', help='Specify LC event log in xml format', required=True)
parser.add_argument('-s','--severity', dest='severity', help='Specify Severity level of the logs: c: critical|w: warning|i: info', required=True)
parser.add_argument('-d','--dcim', dest='dcim', help='Specify name of DCIM XML file', required=True)
args = vars(parser.parse_args())

lc = args['logfile']
sev = args['severity']
dcim = args['dcim']

tree = ET.parse(lc)
severity_dict = {'c': 'Critical', 'w': 'Warning', 'i': 'Informational'}

#Elements list declaration
ctrl_list = ['ProductName', 'ControllerFirmwareVersion']
sys_list = ['Model', 'ChassisServiceTag', 'BIOSVersionString', 'LifecycleControllerVersion']
#ins_dict = {'DCIM_SystemView': sys_list, 'DCIM_ControllerView': ctrl_list}
ins_dict = {'DCIM_SystemView': sys_list}

attrib_list = ['Category', 'Timestamp']
keys_list = ['MessageID', 'Message']
messages = []
sysinfo = []

#Fetch values from element
def getValue(instances, property):
    s = []
    for i in instances:
        for p in property:
            p_xpath = './PROPERTY[@NAME="{0}"]'.format(p)
            v = i.find(p_xpath)
            s.append(v.find('VALUE').text)
            #print("{0}: {1}".format(p, v.find('VALUE').text))
        sysinfo.append(s)

#Define a function to get Version Strings from TSR log
def getVer(dcim):
    tree = ET.parse(dcim)
    for k in ins_dict.keys():
        ins_xpath = './/MESSAGE/SIMPLEREQ/VALUE.NAMEDINSTANCE/INSTANCE[@CLASSNAME="{0}"]'.format(k)
        instances = tree.findall(ins_xpath)
        getValue(instances, ins_dict[k])
        return 0

def getEvent(messageElement):
    i = []
    [ i.append(messageElement.attrib[a]) for a in attrib_list ]
    [ i.append(messageElement.find(k).text) for k in keys_list ]
    messages.append(i)

def timeFormat(message):
    ds = message[1]
    return datetime.datetime.strptime(ds, '%Y-%m-%dT%H:%M:%S%z')

if __name__ == "__main__":
    if sev not in severity_dict.keys():
        parser.print_help()
        exit()
    getVer(dcim)
    xpath_str = './Event[@Severity="{0}"]'.format(severity_dict[sev])
    elist = tree.findall(xpath_str)
    [ getEvent(e) for e in elist ]
    messages_sorted = sorted(messages, key = timeFormat, reverse=True)
    print(T(sysinfo, headers=['Model', 'Service Tag', 'BIOS', 'iDRAC'], tablefmt="psql"))
    print(T(messages_sorted, headers=['Category', 'Timestamp', 'MessageID', 'Message'], tablefmt="psql"))
