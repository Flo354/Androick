#!/usr/bin/python
# -*- coding: utf8 -*-

#<Androick - OWASP Android Project : Forensic analysis helper>
#Copyright (C) <2013 - 2014>  <Florian Pradines>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from subprocess import Popen, PIPE, STDOUT
import getopt
import sys

from general import *
from device import *
from package import *


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ahvAdslmpMD:f:", ["about", "help", "verbose", "all", "datas", "sql", "logs", "manifest", "permissions", "memory-dump" "keyLogs=", "device=", "find="])
	except getopt.GetoptError, err:
		print err
		help()
		sys.exit(2)

	device 		= ""
	find 		= False
	verbose 	= False
	datas 		= False
	sql 		= False
	logs 		= False
	manifest 	= False
	permissions = False
	memoryDump 	= False
	keyLogs 	= []
	
	#Parse options
	for opt, arg in opts:
		if opt in ("-a", "--about"):
			about()
			sys.exit()
		elif opt in ("-h", "--help"):
			help()
			sys.exit()
		elif opt in ("-v", "--verbose"):
			verbose = True
		elif opt in ("-A", "--all"):
			datas 		= True
			sql 		= True
			logs 		= True
			manifest 	= True
			permissions = True
			memoryDump = True
		elif opt in ("-d", "--datas"):
			datas = True
		elif opt in ("-s", "--sql"):
			sql = True
		elif opt in ("-l", "--logs"):
			logs = True
		elif opt in ("--keyLogs"):
			if len(arg) is 0:
				help()
				sys.exit()
			keyLogs = arg.split("|")
		elif opt in ("-m", "--manifest"):
			manifest = True
		elif opt in ("-p", "--permissions"):
			permissions = True
		elif opt in ("-M", "--memory-dump"):
			memoryDump = True
		elif opt in ("-D", "--device"):
			device = "-s "+ arg
		elif opt in ("-f", "--find"):
			find = arg

	if len(args) == 0 and find is False:
		print "Error : no arguments given"
		help()
		sys.exit(2)
	
	if not datas and sql:
		print "Error : option -s (--sql) must be used with -d (--datas)"
		help()
		sys.exit(2)
	
	if not logs and keyLogs:
		print "Error : option --keyLogs must be used with -l (--logs)"
		help()
		sys.exit(2)

	#start adb server
	if verbose:
		print "Starting adb server..."
	process = Popen(["adb", "start-server"], stderr=STDOUT, stdout=PIPE)
	if verbose:
		printVerbose (process)
	else:
		process.communicate()
	
	#validate given device (if given)
	if device != "" and not issetDevice (device):
		print "Device not found"
		sys.exit(2)

	#find package if asked
	if find:
		package = Package(find, device)
		result = package.find()
		if not result:
			print "no packages found with this name"
			sys.exit()
		else:
			print "packages found with this name : "
			i = 1
			for package in result:
				print str(i) +") "+ package
				i += 1
			
			choices = raw_input("Which packages do you want extract. Ex: 1 3 6 (type 0 to quit) : ").split()
			if choices[0] is "0":
				sys.exit(0)
				
			args = []
			for choice in map(int,choices):
				if choice < 1 or choice > len(result):
					print str(choice) +" is not a good value"
				else:
					args.append(result[choice - 1])
	
	#parse & extract packages
	i = 0
	for arg in args:
		package = Package(arg, device)
		
		if len(keyLogs) > i:
			key = keyLogs[i].split(",")
			key.append(arg)
		elif logs:
			key = [arg]
		else:
			key = []
		
		package.extract(verbose, datas, sql, key, manifest, permissions, memoryDump)
		i += 1

if __name__ == "__main__":
	main ()
