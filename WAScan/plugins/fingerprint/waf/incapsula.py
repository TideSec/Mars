#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I 

def incapsula(headers,content):
	_ = False
	for header in headers.items():
		_ |= search(r'incap_ses|visid_incap',header[1],I) is not None
		_ |= search(r'incapsula',header[1],I) is not None
		if _:break
	_ |= search(r'Incapsula incident ID',content) is not None
	if _ : 
		return "Incapsula Web Application Firewall (Incapsula/Imperva)"