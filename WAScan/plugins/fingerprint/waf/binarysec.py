#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I

def binarysec(headers,content):
	_ = False
	for header in headers.items():
		_ |=  header[0].lower() == "x-binarysec-via"
		_ |=  header[0].lower() == "x-binarysec-nocache"
		_ |= search(r'binarySec',header[1],I) is not None
		if _: break
	if _ : 
		return "BinarySEC Web Application Firewall (BinarySEC)"