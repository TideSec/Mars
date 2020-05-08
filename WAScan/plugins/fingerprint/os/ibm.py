#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I 

def ibm(headers):
	os = ['IBM','Lotus-Domino','WebSEAL']
	for o in os:
		for header in headers.items():
			if search(o,header[1],I):
				return "IBM"