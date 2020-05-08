#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I

def dotdefender(headers,content):
	_ = False
	for header in headers.items():
		_ |= header[0] == "x-dotdefender-denied"
		if _: break
	_ |= search(r"dotDefender Blocked Your Request",content) is not None
	if _ : 
		return "dotDefender (Applicure Technologies)"