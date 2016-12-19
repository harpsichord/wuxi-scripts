#!/usr/local/bin/python3.5
#coding: utf-8
#Author: Wu Xi
#Purpose: Dell Warranty API implemented in python
#         Response is in JSON format
#API calls:
#1. Getassetheader
#2. Getassetwarranty
#3. Getassetsummary
#4. Getcodemapping byType
#HTTP methods: only POST method is implemented

import re
import json
import requests
import argparse
from tabulate import tabulate as T

#Create parser
parser = argparse.ArgumentParser(description='Dell Warranty SDK sample code')

#Version Number
ver = '20161219 - Wu Xi'

#Add arguments
parser.add_argument('-s','--servicetag', dest='servicetag', help='Specify a service tag you want to check', required=True)
parser.add_argument('-k','--apikey', dest='apikey', help='Specify APIKEY assigned to you', required=True)
args = vars(parser.parse_args())

dell_apikey=args['apikey']
st=args['servicetag']

gah='https://sandbox.api.dell.com/support/assetinfo/v4/getassetheader'
gaw='https://sandbox.api.dell.com/support/assetinfo/v4/getassetwarranty'
gas = 'https://sandbox.api.dell.com/support/assetinfo/v4/getassetsummary/{0}?apikey={1}'.format(st, dell_apikey)

#r_headers = {'apikey': dell_apikey, 'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'Application/json'}
r_headers = {'apikey': dell_apikey}
payload = {'ID': st}
keys = ['PartDescription', 'Quantity']

def getSD(asset_header):
    try:
        sd=asset_header['AssetHeaderResponse'][0]['AssetHeaderData']['ShipDate']
        i=sd.index('T')
        date_items.append([st, sd[:i]])
    except IndexError as err:
        date_items.append(['N/A', 'N/A'])

def getAW(asset_warranty):
    try:
        for i in asset_warranty['AssetWarrantyResponse'][0]['AssetEntitlementData']:
            sl = i['ServiceLevelDescription']
            sd = i['StartDate'][:10]
            ed = i['EndDate'][:10]
            warranty_items.append([sl, sd, ed])
    except IndexError as err:
        warranty_items.append(['N/A', 'N/A', 'N/A'])


def decodeAssetData(ad):
    match = re.search(r'^Processor,|^PRC,|^HD,|CTL|^DIMM,', ad[keys[0]])
    if match:
        parts_items.append([ad[keys[0]], ad[keys[1]]])

def getAS(assets_summary):
    try:
        asset_data=assets_summary['AssetSummaryResponse']['AssetPartsData']
        [ decodeAssetData(ad) for ad in asset_data ]
    except IndexError as err:
        parts_items.append(['N/A', 'N/A'])


if __name__ == "__main__":
    print("Using ***SANDBOX*** environment of Dell Service API!")
    print("Version: {0}".format(ver))

    #Get ShipDate
    r = requests.post(gah, headers=r_headers, data=payload)
    date_items = []
    asset_header = r.json()
    getSD(asset_header)
    print(T(date_items, headers=['Service Tag', 'Ship Date'], tablefmt="psql"))

    #Get Asset Summary
    r = requests.get(gas)
    parts_items = []
    assets_summary = r.json()
    getAS(assets_summary)
    print(T(parts_items, headers=['Part Description', 'Quantity'], tablefmt="psql"))

    #Get Warranty info
    r = requests.post(gaw, headers=r_headers, data=payload)
    warranty_items = []
    asset_warranty = r.json()
    getAW(asset_warranty)
    print(T(warranty_items, headers=['Service level Description', 'Start Date', 'End Date'], tablefmt="psql"))
