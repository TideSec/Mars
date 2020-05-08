#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Thomas Hartmann (thomysec)
# @license: See the file 'LICENSE.txt'

from re import search,I 

def adobeaem(headers,content):
	_  = False
	_ |= search(r"<link[^>]*stylesheet[^>]*etc\/designs\/[^>]*\>[^<]*",content) is not None
	_ |= search(r"<link[^>]*etc\/clientlibs\/[^>]*\>[^<]*",content) is not None
	_ |= search(r"<script[^>]*etc\/clientlibs\/[^>]*\>[^<]*",content) is not None
	_ |= search(r"<script[^>]*\/granite\/[^>]*(\.js\")+\>[^<]*",content) is not None
	if _ : return "Adobe AEM: Stack is based on Apache Sling + Apache Felix OSGi container + JCR Repo + Java"