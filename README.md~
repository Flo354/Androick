# Androick

Androick is a python tool to help in forensics analysis on android.
Put the package name, some options and the programm will download automatically apk, datas, files permissions, manifest, databases and logs.
It is easy to use and avoid all repetitives tasks !


## Installation
Simply clone this git repository

### Dependencies

#### Python
-	python >= 2.6
-	[Python-magic](https://github.com/ahupp/python-magic/)

#### SDK
-	aapt
-	adb
-	hprof-conv

#### Others
-	a rooted device
-	sqlite3	

## How to use
	1) show help message
		./androick.py -h

	2) show informations
		./androick.py -a

	3) select device to use
		./androick.py -D serial_number PACKAGE_NAME_1 PACKAGE_NAME_2 ETC...
		./androick.py --device serial_number PACKAGE_NAME_1 PACKAGE_NAME_2 ETC...

	4) find package name
		./androick.py [-v] -f <Part of package name>

	5) download all related things of application
		./androick.py [-v] -A PACKAGE_NAME_1 PACKAGE_NAME_2 ETC...
	
	6) select only things you want extract
		./androick.py [-v] [-d --datas] [-s --sql] [-m --manifest] [-p --permissions] [-m --memory-dump]  [-l --logs] [--keyLogs="keywords"] PACKAGE_NAME_1 PACKAGE_NAME_2 ETC...

	7) how to use option --keyLogs
			--keyLogs="key1,key2,key3"
		if more than one package
			--keyLogs="key1_P1,key2_P1|key1_P2|key1_P3,key2_P3,key3_P3"
		
		Example :
			./androick.py -l --keyLogs="antivirus,protection|music,licence" com.package.antivirus com.music.player
	
	/!\ The memory dump option will mostly not works with production builds

## Author
Written by Florian Pradines (Phonesec), this tool is a referenced OWASP Android security project since 2013.

You can contact me via my [website](http://florianpradines.com)

## Licence
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
