#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from re import search,I 

def silverstripe(headers,content):
	_  = False
	if 'set-cookie' in headers.keys():
		_ |= search(r"PastVisitor=[0-9]+.*",headers["set-cookie"],I) is not None
	_ |= search(r"\<meta name\=\"generator\"[^>]*content\=\"SilverStripe",content) is not None
	_ |= search(r"\<link[^>]*stylesheet[^>]*layout.css[^>]*\>[^<]*\<link[^>]*stylesheet[^>]*typography.css[^>]*\>[^<]*\<link[^>]*stylesheet[^>]*form.css[^>]*\>",content) is not None
	_ |= search(r"\<img src\=\"\/assets\/[^\/]+\/_resampled\/[^\"]+.jpg\"",content) is not None
 	if _ : return "SilverStripe"