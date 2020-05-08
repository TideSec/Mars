#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search,I

def cloudflare(headers,content):
	_ = False
	for header in headers.items():
		_ |=  header[0].lower() == "cf-ray"
		_ |= search(r'__cfduid=|cloudflare-nginx|cloudflare[-]',header[1],I) is not None
		if _: break
	_ |= search(r"CloudFlare Ray ID:|var CloudFlare=",content) is not None
	if _ : 
		return "CloudFlare Web Application Firewall (CloudFlare)"