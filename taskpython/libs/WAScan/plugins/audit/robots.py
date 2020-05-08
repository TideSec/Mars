#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from re import findall,I
from lib.utils.check import *
from lib.utils.printer import *
from lib.utils.readfile import *
from lib.request.request import *

class robots(Request):
	""" check robots path  """
	get = "GET"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 
		self.data = data

	def run(self):
		""" Run """
		info('Checking robots...')
		paths = []
		# check url path
		url = CPath(self.url,'robots.txt')
		# send request
		req = self.Send(url=url,method=self.get)
		# if status code == 200 and req.url == url
		if req.code == 200 and CEndUrl(req.url) == url:
			# and req.content != ""
			if req.content != "":
				# findall all robots (allow:.../disallow:...) paths
				paths += findall(r'[disallow]\: (\S*)',req.content)
		if paths != None and paths != "":
			for path in paths:
				# check url path
				url = CPath(self.url,path)
				# send request 
				req = self.Send(url=url,method=self.get)
				# print code and url
				more('[%s] %s'%(req.code,req.url))