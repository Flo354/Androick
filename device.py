#!/usr/bin/python
# -*- coding: utf8 -*-

from subprocess import Popen, PIPE, STDOUT
import sys

def issetDevice(device):
	cmd = "adb "+ device +" get-state"
	process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
	stdout, stderr = process.communicate()
	if stdout == "device\n":
		return True
	return False
