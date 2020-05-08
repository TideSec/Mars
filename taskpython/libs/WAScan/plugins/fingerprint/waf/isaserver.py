#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I 

def isaserver(headers,content):
	_ = False
	_ |= search(r'The server denied the specified Uniform Resource Locator (URL). Contact the server administrator.',content) is not None
	_ |= search(r'The ISA Server denied the specified Uniform Resource Locator (URL)',content) is not None
	if _ : 
		return "ISA Server (Microsoft)"