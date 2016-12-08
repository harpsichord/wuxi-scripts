#!/usr/local/bin/python3.5
#coding: utf-8
#Author: Wu Xi
#Purpose: LifeCycle(contained in TSR log) log analyzer

#from tabulate import tabulate as T
import xml.etree.ElementTree as ET
import argparse
from tabulate import tabulate as T

#Create parser
parser = argparse.ArgumentParser(description='LifeCycle events analyzer')

#Add arguments
parser.add_argument('-f','--logfile', dest='logfile', help='Specify LC event log in xml format', required=True)
parser.add_argument('-s','--severity', dest='severity', help='Specify Severity level of the logs: c: critical|w: warning|i: info', required=True)
args = vars(parser.parse_args())

lc = args['logfile']
sev = args['severity']

tree = ET.parse(lc)
severity_dict = {'c': 'Critical', 'w': 'Warning', 'i': 'Informational'}

attrib_list = ['Category', 'Timestamp']
keys_list = ['MessageID', 'Message']
messages = []

def getEvent(messageElement):
    i = []
    [ i.append(messageElement.attrib[a]) for a in attrib_list ]
    [ i.append(messageElement.find(k).text) for k in keys_list ]
    messages.append(i)

if __name__ == "__main__":
    if sev not in severity_dict.keys():
        parser.print_help()
        exit()
    xpath_str = './Event[@Severity="{0}"]'.format(severity_dict[sev])
    elist = tree.findall(xpath_str)
    [ getEvent(e) for e in elist ]
    print(T(messages, headers=['Category', 'Timestamp', 'MessageID', 'Message'], tablefmt="psql"))
