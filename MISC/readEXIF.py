#!/usr/local/bin/python3.5

import exifread as er
import argparse
from tabulate import tabulate as T

#Create parser
parser = argparse.ArgumentParser(description='EXIF reader')

#Add arguments
parser.add_argument('-f','--filename', dest='filename', help='Specify name of the image you want to process', required=True)
args = vars(parser.parse_args())

fn = args['filename']

tags_dict = {'Image Model': 'Camera Model', 'EXIF Flash': 'Flash', 'EXIF ShutterSpeedValue': 'Shutter Speed', 'EXIF ISOSpeedRatings': 'ISO setting', 'EXIF LensModel': 'Lens Model'}
exif_items = []

def getEXIF():
    p = open(fn, 'rb')
    tags = er.process_file(p, details=False)
    [ exif_items.append([tags_dict[tag], tags[tag]]) for tag in tags_dict.keys() ]

if __name__ == "__main__":
    print("{0}:\t{1}".format("EXIF reader", "Wu Xi"))
    exif_items.append(['Image Name', fn])
    getEXIF()
    print(T(exif_items, headers=['Tag name', 'Value'], tablefmt="psql"))
