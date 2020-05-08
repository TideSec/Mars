#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from lib.utils.check import *
from lib.utils.printer import *
from lib.request.request import *

class apache(Request):
	""" Apache """
	get = "GET"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url
		self.data = data

	def run(self):
		"""Run"""
		info('Checking Apache Status Page...')
		paths = ['perl-status','server-status','server-info',
				 'stronghold-info','stronghold-status']
		for path in paths:
			# check url path
			url = CPath(self.url,path)
			# send request 
			req = self.Send(url=self.url,method=self.get)
			# if status code  == 200
			if req.code == 200:
				# and req.url == url 
				if CEndUrl(req.url) == url:
					plus("A potential apache \"%d\" enabled at: %s"%(path,req.url))
