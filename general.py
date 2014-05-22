#!/usr/bin/python
# -*- coding: utf8 -*-

from subprocess import Popen, PIPE, STDOUT
import sys

def about():
	print "####################################################"
	print "#	@author		Florian Pradines	   #"
	print "#	@company	Phonesec		   #"
	print "#	@mail		f.pradines@phonesec.com	   #"
	print "#	@mail		florian.pradines@owasp.org #"
	print "#	@version	2.0			   #"
	print "#	@licence	GNU GPL v3		   #"
	print "#	@dateCreation	27/03/2013		   #"
	print "#	@lastModified	12/09/2013		   #"
	print "####################################################"
	print ""
	print "Androick is a helper for forensics analysis on android."

def help():
	print "Usage : "+ sys.argv[0] +" [OPTIONS] PACKAGE_NAME_1 [PACKAGE_NAME_2 etc...]"
	print "-a --about : more informations about this program"
	print "-h --help : display this message"
	print "-v --verbose : verbose mode"
	print "-D --device : serial number of the device"
	print "-A --all : activate all options"
	print "-d --datas : get datas from the applications"
	print "-s --sql : find and export all databases in csv (must be used with -d)"
	print "-m --manifest : generate a minimal manifest file"
	print "-p --permissions : get all permissions of application's file"
	print "-M --memory-dump : get a memory heap dump from the application"
	print "  => will mostly not works on production builds"
	print "-l --logs : getting logs from application"
	print "--keyLogs : Choose your logs keywords (default : PACKAGE_NAME, must be used with -l)"
	print "\tExample : --keyLogs=\"key1,key2,key3\""
	print "  if more than one package you can choose keywords for each package by doing : "
	print "\t--keyLogs=\"key1_P1,key2_P1|key1_P2|key1_P3,key2_P3,key3_P3\" etc..."
	print "-f --find : find a package"
	print ""
	print ""
	print "1) show help message"
	print "\t./androick.py -h"
	print ""
	print "2) show informations"
	print "\t./androick.py -a"
	print ""
	print "3) select device to use"
	print "\t./androick.py -D serial_number PACKAGE_NAME_1 PACKAGE_NAME_2 ETC..."
	print "\t./androick.py --device serial_number PACKAGE_NAME_1 PACKAGE_NAME_2 ETC..."
	print ""
	print "4) find package name"
	print "\t./androick.py [-v] -f <Part of package name>"
	print ""
	print "5) download all related things of application"
	print "\t./androick.py [-v] -A PACKAGE_NAME_1 PACKAGE_NAME_2 ETC..."
	print ""
	print "6) select only things you want extract"
	print "\t./androick.py [-v] [-d --datas] [-s --sql] [-m --manifest] [-p --permissions] [-M --memory-dump] [-l --logs] [--keyLogs=\"keywords\"] PACKAGE_NAME_1 PACKAGE_NAME_2 ETC..."
	print ""
	print "7) Example with option --keyLogs"
	print "\t./androick.py -l --keyLogs=\"antivirus,protection|music,licence\" com.package.antivirus com.music.player"
	
def printVerbose (process):
	while process.poll() is None:
		print process.stdout.readline().replace("\n", "").replace("\r", "")
	process.communicate()


def writeResultToFile (cmd, filename, verbose):
	try:
		f = open(filename, "w")
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		
		while True:
			line = process.stdout.readline()
			if not line:
				break
			
			f.write(line)
			
			if verbose:
				print line.replace("\n", "").replace("\r", "")
		
		process.communicate()
		f.close()
		
		return True
	except IOError as e:
		print "File " + e.filename +" not created"
		print "Exception : "+ e.strerror
