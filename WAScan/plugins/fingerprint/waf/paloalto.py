#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I 

def paloalto(headers,content):
	_ = False
	_ |= search(r'Access[^<]+has been blocked in accordance with company policy',content) is not None
	if _ : 
		return "Palo Alto Firewall (Palo Alto Networks)"