#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import findall,I

def flash(content):
	_ = findall(r'\<a href\=\S*(\.swf)',content,I)
	if _ != []: return "Flash"