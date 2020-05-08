#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from re import search,I 

def drupal(headers,content):
	_  = False
	if 'set-cookie' in headers.keys():
		_ |= search(r"SESS[a-z0-9]{32}=[a-z0-9]{32}",headers["set-cookie"],I) is not None
	if 'x-drupal-cache' in headers.keys():_ |= True
	_ |= search(r"\<script type\=\"text\/javascript\" src\=\"[^\"]*\/misc\/drupal.js[^\"]*\"\>\<\/script\>",content) is not None
	_ |= search(r"<[^>]+alt\=\"Powered by Drupal, an open source content management system\"",content) is not None
	_ |= search(r"@import \"[^\"]*\/misc\/drupal.css\"",content) is not None
	_ |= search(r"jQuery.extend\(drupal\.S*",content) is not None
	_ |= search(r"Drupal.extend\(\S*",content) is not None
	if _ : return "Drupal"