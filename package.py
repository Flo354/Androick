#!/usr/bin/python
# -*- coding: utf8 -*-

from subprocess import Popen, PIPE, STDOUT
import os
import sys
import datetime
import time
import fnmatch
import magic

from general import *

class Package():
	def __init__(self, package, device):
		self.device 	= device
		self.package 	= package

	# find packages
	def find(self):
		cmd = "adb "+ self.device +" shell pm list packages " + self.package
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		stdout, stderr = process.communicate()
		if stdout == "":
			return False
		else:
			return stdout.replace("package:", "").split()
	
	# check if package exist
	def exist(self):
		print "\nVerifying if package '" + self.package + "' exist..."
		
		result = self.find()
		if result and self.package in result:
			if self.verbose:
				print "Package exist\n"
			return True
		
		print "Package "+ self.package +" not found"
		return False
	
	# extract datas
	def extract(self, verbose, datas, sql, keyLogs, manifest, permissions, memoryDump):
		self.verbose = verbose
		
		if not self.exist():
			return False
		
		self.externalStorage = self.getExternalStorage()
		
		self.createDirectories()
		self.getAPK()
		
		if datas:
			self.getDatas()
			self.getExternalDatas()
			self.getExternalDatasSD()
			self.getLib()
		
		if sql:
			self.getSQL()
		
		if manifest:
			self.getManifest()		
		
		if permissions:
			self.getPermissions()
		
		if memoryDump:
			self.getMemoryDump()
		
		if len(keyLogs) > 0:
			self.getLogs(keyLogs)
		
		return True
		
	def createDirectories(self):
		#create directories
		try:
			self.path = "output/"+ self.package
			if os.path.exists (self.path):
				self.path = "output/"+ self.package +"-"+ datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
			
			self.pathData = self.path + "/data"
			self.pathDataSD = self.path + "/dataSD"
			self.pathDataExternalSD = self.path + "/dataExternalSD"
			self.pathLib = self.path + "/lib"
			self.pathSQL = self.path + "/SQL"
			self.pathLogs = self.path + "/Logs"
			
			if not self.verbose:
				print "Creating directories..."
			
			if self.verbose:
				print "Creating directory : "+ self.pathData
			os.makedirs(self.pathData)
			if self.verbose:
				print "Creating directory : "+ self.pathDataSD
			os.makedirs(self.pathDataSD)
			if self.verbose:
				print "Creating directory : "+ self.pathDataExternalSD
			os.makedirs(self.pathDataExternalSD)
			if self.verbose:
				print "Creating directory : "+ self.pathLib
			os.makedirs(self.pathLib)
			if self.verbose:
				print "Creating directory : "+ self.pathSQL
			os.makedirs(self.pathSQL)
			if self.verbose:
				print "Creating directory : "+ self.pathLogs +"\n"
			os.makedirs(self.pathLogs)
		except OSError as e:
			print "Folder " + e.filename +" not created"
			print "Exception : "+ e.strerror
	
	def getAPK(self):
		if self.verbose:
			print "Getting APK Path..."
		#getting apk path
		cmd = "adb "+ self.device +" shell pm path "+ self.package
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		stdout, stderr = process.communicate()
		self.pathToApk = stdout.replace("package:", "")
		if self.verbose:
			print "APK Path : " + self.pathToApk
		
		#pull apk to computer
		print "Downloading APK..."
		cmd = "adb pull "+ self.pathToApk +" "+ self.path + "/" + self.package + ".apk"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		if self.verbose:
			printVerbose (process)
		else:
			process.communicate()
		
		cmd = "adb pull "+ self.pathToApk.replace(".apk", ".odex") +" "+ self.path + "/" + self.package + ".odex"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		if self.verbose:
			printVerbose (process)
		else:
			process.communicate()
		
		print ""
	
	def getDatas(self):
		print "Downloading datas..."
			
		if self.verbose:
			print "Create temporary directory"
		cmd = "adb "+ self.device +" shell su -c rm -rf /sdcard/androick/*;mkdir -p /sdcard/androick/"+ self.package
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		
		if self.verbose:
			print "Copy datas to temporary directory"
		cmd = "adb "+ self.device +" shell su -c cp -r /data/data/"+ self.package +" /sdcard/androick/"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		
		if self.verbose:
			print "Pull datas to computer"
		cmd = "adb "+ self.device +" pull /sdcard/androick/"+ self.package +" "+ self.pathData
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		if self.verbose:
			printVerbose (process)
		else:
			process.communicate()
		
		if self.verbose:
			print "Remove temporary directory"
		cmd = "adb "+ self.device +" shell rm -rf /sdcard/androick"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE, stdin=PIPE)
		process.communicate()
		print ""
	
	# find external sd storage path
	def getExternalStorage(self):
		if self.verbose:
			print "Getting external storage path..."
			
		cmd = "adb "+ self.device +" shell echo $EXTERNAL_STORAGE"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		stdout, stderr = process.communicate()
		if stdout == "":
			if self.verbose:
				print "external directory not found\n"
			return False
		else:
			if self.verbose:
				print "external directory : " + stdout
			return stdout.replace("\n", "").replace("\r", "")
	
	# download external datas
	def getExternalDatas(self):
		print "Downloading external datas..."
		
		cmd = "adb "+ self.device +" pull /sdcard/Android/data/"+ self.package +" "+ self.pathDataSD
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		
		if self.verbose:
			printVerbose (process)
		else:
			process.communicate()
		print ""
	
	# download external SD card datas
	def getExternalDatasSD(self):
		print "Downloading external SD card datas..."
		
		if self.externalStorage:
			cmd = "adb "+ self.device +" pull "+ self.externalStorage + "/Android/data/"+ self.package +" "+ self.pathDataExternalSD
			process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
			
			if self.verbose:
				printVerbose (process)
			else:
				process.communicate()
		print ""
	
	# download libraries (only for applications who are stored in external SD card)
	def getLib(self):
		if self.pathToApk.find("/data/data/", 0, 11) is -1:
			print "downloading libraries files..."
			
			cmd = "adb "+ self.device +" pull "+ self.pathToApk.replace("pkg.apk", "lib") +" "+ self.pathLib
			process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
			
			if self.verbose:
				printVerbose (process)
			else:
				process.communicate()
		print ""
	
	# extract databases in csv format
	def getSQL(self):
		print "Finding databases files..."
		mime = magic.Magic()
		for root, dirnames, filenames in os.walk(self.path):
		  for filename in fnmatch.filter(filenames, "*"):
		  	try:
			  	typeFile = mime.from_file(root +"/"+ filename)
				if typeFile is not None and typeFile.find("SQLite", 0, 6) is not -1:
				  	if self.verbose:
				  		print "Database found : "+ root +"/"+ filename
				  	
				  	os.makedirs(self.pathSQL + "/" + filename)
				  	
				  	cmd = "sqlite3 "+ root +"/"+ filename +" .tables"
				  	process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
				  	stdout, stderr = process.communicate()

				  	cmd = "sqlite3 "+ root +"/"+ filename
					process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE, stdin=PIPE)
					process.stdin.write(".headers on\n")
					process.stdin.write(".mode csv\n")
				  	for table in stdout.split():
				  		if self.verbose:
				  			print "\tExtracting table : "+ table
						process.stdin.write(".output "+ self.pathSQL +"/"+ filename +"/"+ table +".csv\n")
						process.stdin.write("select * from "+ table +";\n")
					process.stdin.write(".quit\n")
					stdout, stderr = process.communicate()
			except IOError:
				continue
			except OSError as e:
				print "Folder " + e.filename +" not created"
				print "Exception : "+ e.strerror
		print ""
	
	def getManifest(self):
		print "Generating manifest..."
		cmd = "aapt d badging " + self.path + "/" + self.package + ".apk"
		writeResultToFile(cmd, self.path + "/informations", self.verbose)
		
		cmd = "aapt d xmltree " + self.path + "/" + self.package + ".apk" + " AndroidManifest.xml"
		writeResultToFile(cmd, self.path + "/manifest", self.verbose)
		print ""
	
	def getPermissions(self):
		print "Getting files permissions..."
		cmd = "adb " + self.device + " shell su -c 'ls -aRl /data/data/" + self.package + " /sdcard/Android/data/" + self.package + "'"
                if self.externalStorage:
                    cmd = cmd[:-1] + " " + self.externalStorage + "/Android/data/"+ self.package + "'"
		writeResultToFile(cmd, self.path + "/permissions", self.verbose)
		print ""
	
	def getMemoryDump(self):
		print "Getting heap memory dump..."
		
		if self.verbose:
			print "Getting PID column number..."
		cmd = "adb " + self.device + " shell su -c ps | head -n 1 | awk -F' ' '{for (i = 1; i <= NF; i++) if ($i == \"PID\") print i}'"
		process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
		column, stderr = process.communicate()
		column = column.replace("\n", "").replace("\r", "")

		try:
			column = int(column)
		except ValueError:
			print "Error : PID column not found. Cannot get memory dump.\n"
			return False

		if self.verbose:
			print "Opening application (don't close it until the end of program...)"
		cmd = "adb shell monkey -p " + self.package + " -v 1"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE, stdin=PIPE)
		process.communicate()
		
		if self.verbose:
			print "Search application PID..."
		cmd = "adb " + self.device + " shell su -c ps | awk -F' ' '{if ($NF == \"" + self.package + "\r\") print $" + str(column) +"}'"
		process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
		pid, stderr = process.communicate()
		pid = pid.replace("\n", "").replace("\r", "")
		
		try:
			pid = int(pid)
		except ValueError:
			print "Error : PID not found. Cannot get memory dump.\n"
			return False
		
		if self.verbose:
			print "Generating memory dump..."
		cmd = "adb " + self.device + " shell su -c am dumpheap " + str(pid) + " /sdcard/androick-memory-heap-dump"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE, stdin=PIPE)
		stdout, stderr = process.communicate()

		if len(stdout) > 1 or stderr is not None:
			print "Error : cannot generate memory dump.\n"
			return False
		
		if self.verbose:
			print "Pull memory dump to computer..."
		cmd = "adb "+ self.device +" pull /sdcard/androick-memory-heap-dump " + self.path + "/memory-heap-dump"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		
		if self.verbose:
			print "Removing memory dump from phone..."
		cmd = "adb "+ self.device +" shell rm /sdcard/androick-memory-heap-dump"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		
		if self.verbose:
			print "Converting dump to hprof format..."
		cmd = "hprof-conv " + self.path + "/memory-heap-dump " + self.path + "/memory-heap-dump.hprof"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		
		cmd = "rm " + self.path + "/memory-heap-dump"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		print ""		
		
	def getLogs(self, keyLogs):
		print "Getting logs"
		for key in keyLogs:
			if self.verbose:
				print "Getting logs corresponding to : " + key
			
			cmd = "adb " + self.device + " logcat -d | grep " + key
			writeResultToFile(cmd, self.pathLogs + "/" + key, self.verbose)
	
