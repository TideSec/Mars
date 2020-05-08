#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I

def bigip(headers,content):
	_ = False
	for header in headers.items():
		_ |=  header[0].lower() == "x-cnection"
		_ |=  header[0].lower() == "x-wa-info"
		_ |= search(r'\ATS\w{4,}=|bigip|bigipserver|\AF5\Z',header[1],I) is not None
		if _: break
	if _ : 
		return "BIG-IP Application Security Manager (F5 Networks)"