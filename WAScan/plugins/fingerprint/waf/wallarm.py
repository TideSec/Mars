#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I 

def wallarm(headers,content):
	_ = False
	_ |= headers['server'] == 'nginx-wallarm'
	if _ : 
		return "Wallarm Web Application Firewall (Wallarm)" 