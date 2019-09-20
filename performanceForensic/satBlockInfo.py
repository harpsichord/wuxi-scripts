#!/usr/bin/env python
#Author: Wu Xi
#Date: 09/12/2019
#Purpose: Get various attributes of block devices in the system, hopefully it can manage to collect data from HDD, SSD, NVME, ... eventually.

import json
import argparse
from jsonpath_rw import jsonpath
from jsonpath_rw_ext import parse
import jsonpath_rw_ext as jp

def wxPrint(d, kn):
    print("{0}: {1}".format(kn, d[kn]))

def getValues(co, k_list):
    if type(co) is list:
        for l in co:
            for i in k_list:
                wxPrint(l, i)
    elif type(co) is dict:
        for i in k_list:
            wxPrint(co, i)
    else:
        print('Invalid object!!!')

def wxDictIterator(infoDict, wxObj):
    for idk in infoDict.keys():
        comm_obj = wxObj[0][idk]
        getValues(comm_obj, infoDict[idk])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Various information of block devices')
    parser.add_argument('--slotInfo', help='location of slot info file', required=True)
    parser.add_argument('--ctrlInfo', help='location of controller info file', required=True)
    parser.add_argument('--encInfo', help='location of enclosure info file', required=True)

    args = parser.parse_args()
    s = args.slotInfo
    c = args.ctrlInfo
    e = args.encInfo

    #Common json path string
    cmd_jpath = "$.Controllers[0].'Command Status'[Status]"
    rsp_jpath = "$.Controllers[0].'Response Data'"

    #Controller information
    with open(c) as ci:
        json_data = json.load(ci)
        cc = jp.match(cmd_jpath, json_data)[0]
        print("Controller command Status: {}".format(cc.encode('ascii')))
        o = jp.match(rsp_jpath, json_data)

        status_list = ['Current Personality', 'Controller Status']
        ver_list = ['Firmware Package Build', 'Driver Version']
        basic_list = ['Model', 'Mfg Date', 'Revision No']
        pd_list = ['EID:Slt', 'State']
        ctrl_dict = {'Version': ver_list, 'Basics': basic_list, 'PD LIST': pd_list, 'Status': status_list}

        wxDictIterator(ctrl_dict, o)

    print("------")

    #Enclosure information
    with open(e) as ei:
        json_data = json.load(ei)
        ec = jp.match(cmd_jpath, json_data)[0]
        print("Enclosure command Status: {}".format(ec.encode('ascii')))
        o = jp.match(rsp_jpath, json_data)

        prop_list = ['EID', 'State']
        enc_dict = {'Properties': prop_list}

        wxDictIterator(enc_dict, o)

    print("------")

    #Physical disks information
    with open(s) as si:
        json_data = json.load(si)
        sc = jp.match(cmd_jpath, json_data)[0]
        print("Slot command Status: {}".format(sc.encode('ascii')))
        o = jp.match(rsp_jpath, json_data)
        for k in o[0].keys():
            print(k, type(o[0][k]))
