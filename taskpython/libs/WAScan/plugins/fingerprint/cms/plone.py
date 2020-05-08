#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from re import search,I 

def plone(headers,content):
	_  = False
	if 'x-caching-rule-id' in headers.keys():
		_ |= search(r"plone-content-types",headers["x-caching-rule-id"],I) is not None
	if 'x-cache-rule' in headers.keys():
		_ |= search(r"plone-content-types",headers["x-cache-rule"],I) is not None
	_ |= search(r"\<meta name\=\"generator\" content\=\"[^>]*http:\/\/plone.org\" \/>",content) is not None
	_ |= search(r"(@import url|text\/css)[^>]*portal_css\/.*plone.*css(\)|\")",content) is not None
	_ |= search(r"src\=\"[^\"]*ploneScripts[0-9]+.js\"",content) is not None
	_ |= search(r"\<div class\=\"visualIcon contenttype-plone-site\"\>",content) is not None
 	if _ : return "Plone"