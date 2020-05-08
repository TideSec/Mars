#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I 

def sitelock(headers,content):
	_ = False
	_ |= search(r"SiteLock Incident ID",content) is not None
	if _ : 
		return "TrueShield Web Application Firewall (SiteLock)"