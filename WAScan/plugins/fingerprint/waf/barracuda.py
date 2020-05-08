#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I

def barracuda(headers,content):
	_ = False
	for header in headers.items():
		_ |= search(r'\Abarra_counter_session=|(\A|\b)barracuda_',header[1],I) is not None
		if _ : break
	if _:
		return "Barracuda Web Application Firewall (Barracuda Networks)"