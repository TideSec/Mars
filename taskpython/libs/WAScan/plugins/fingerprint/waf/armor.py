#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I

def armor(headers,content):
	_ = False
	_ |= search(r'This request has been blocked by website protection from Armor',content,I) is not None
	if _ : 
		return "Armor Protection (Armor Defense)" 