#!/usr/local/bin/python
import os,sys,time
import re

try:
    import _pickle as cPickle
except:
    import cPickle
	
if not os.path.exists('./ServerNum/temp/'):
        os.system("mkdir ./ServerNum/temp/ -p")


def getSmartlog():
	driveInf=[]

	nowtime = str(int(time.time()))
	dir = "./ServerNum/temp/"

	#search the drive's information
	cmd = "fdisk -l >./ServerNum/temp/driveInf.txt"
	os.system(cmd)

	#search how many drives in the server,such as /dev/sdx
	f = open("./ServerNum/temp/driveInf.txt")
	driveMs= re.compile(r"(/dev/sd.*\B)") 
	for line1 in f:
		Ms1=re.search(driveMs,line1)
		if Ms1:
			driveStr=Ms1.group(0).split(":")[0].strip()
			driveInf.append(driveStr)
	f.close()


	#get each drvie's smartctl
	for i in range(len(driveInf)):
		nowtime = str(int(time.time()))
		cmd = "smartctl -a  %s>./ServerNum/temp/smart.txt" %driveInf[i]
		os.system(cmd)

		f = open("./ServerNum/temp/smart.txt")
		for line in f:
			if  ("Serial Number:" in line):
		        	serialnum = line.split("Serial Number:")[1].strip()
		        	if len(serialnum)>8:
		                	serialnum = serialnum[:8]
			if  ("Serial number:" in line):
		        	serialnum = line.split("Serial number:")[1].strip()
		        	if len(serialnum)>8:
		                	serialnum = serialnum[:8]
			if "Device Model:" in line:
	    			modelnum = line.split("Device Model:")[1].strip()
			if "Device model:" in line:
				modelnum = line.split("Device model:")[1].strip()
		f.close()
	
		#Change the fileName according to the drive's Module/SN
		# !!!To be updated by customer here!!!
		# !!!To be updated by customer here!!!
		# !!!To be updated by customer here!!!
		filename = "./ServerNum/"+modelnum+"_"+serialnum+ "_"+time.strftime("%Y%m%d%H%M%S", time.localtime())+".txt"
		cmd = "mv ./ServerNum/temp/smart.txt %s" %filename  
		os.system(cmd)

	cmd = "rm -rf  ./ServerNum/temp"  
	os.system(cmd)

getSmartlog()
