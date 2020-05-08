#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt


from lib.utils.printer import *
from lib.handler.audit import *
from lib.handler.brute import *
from lib.handler.attacks import *
from lib.handler.disclosure import *

def FullScan(kwargs,url,data):
	info('Starting full scan...')
	if '?' in url:
		Attacks(kwargs,url,data)
	# Disclosure(kwargs,url,data)