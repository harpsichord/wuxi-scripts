#!/usr/bin/env python

from __future__ import print_function
import json
from pprint import pprint
import re
import argparse
import time
from collections import OrderedDict

#from tabulate import tabulate

#res list contains two members:
#key:
#    0 - Hardware error
#    1 - Software error
#    2 - No pattern found, need to review the original vmcore-dmesg
#Value:
#    detailed info of the error

#default: nothing found
r = []

def vmcoreAnalyze(err_dict, vmcore):
    for (k, v) in err_dict.items():
#        pattern = re.escape(k.encode('ascii'))
        pattern = r".*" + k.encode('ascii') + ".*"
#        print(pattern)
        x = re.search(pattern, vmcore)
        rl = ""
        if x:
            rl = x.group(0)
            return v, rl
        else:
            return None, None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Take in vmcore-dmesg file')
    parser.add_argument('--vmcore', help='location of vmcore-dmesg file', required=True)

    args = parser.parse_args()
    f = args.vmcore 
    t = open(f, 'r')
    vmcore = t.read()
    t.close()

    f = 'config/err_dict.json'
    with open(f) as c:
        config = json.load(c, object_pairs_hook=OrderedDict)

    for k in config.keys():
        err = config[k]
#        r = vmcoreAnalyze(err, vmcore)
        r, raw_log = vmcoreAnalyze(err, vmcore)
        time.sleep(1)
        if r:
            break

    if r:
        print(r[1], end=',')
        if int(r[0]) == 0:
            print("Hardware error", end=',')
        else:
            print("Software error", end=',')
        print(raw_log)

    else:
        print('Review original vmcore-dmesg')
