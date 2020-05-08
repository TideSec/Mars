#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I 

def windows(headers):
	os = ["windows","win32"]
	for o in os:
		for header in headers.items():
			if search(o,header[1],I):
				return o.title()