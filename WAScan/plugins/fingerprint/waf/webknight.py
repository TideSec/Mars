#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I 

def webknight(headers,content):
	_ = False
	_ |= headers['server'] == 'WebKnight'.lower()
	if _ : 
		return "WebKnight Application Firewall (AQTRONIX)"