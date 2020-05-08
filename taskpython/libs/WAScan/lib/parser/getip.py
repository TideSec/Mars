#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

import re

def getip(content):
	"""Private IP"""
	IP_LIST = re.findall(r'[0-9]+(?:\.[0-9]+){3}',content,re.I)
	if IP_LIST != None or IP_LIST != []:
		return IP_LIST