#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I

def comodo(headers,content):
	_ = False
	for header in headers.items():
		_ |= search(r'protected by comodo waf',header[1],I) is not None
		if _: break
	if _ : 
		return "Comodo Web Application Firewall (Comodo)"