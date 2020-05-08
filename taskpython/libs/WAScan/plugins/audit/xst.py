#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from re import search,I
from lib.utils.printer import *
from lib.request.request import *

class xst(Request):
	""" xst """
	# method
	trace = "TRACE"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url
		self.data = data

	def run(self):
		"""Run"""
		info('Checking Cross Site Tracing...')
		# headers 
		headers = {
					'Fuck':'Hello_Word'
					}
		# send request 
		req = self.Send(url=self.url,method=self.trace,headers=headers)
		# 
		regexp = r"*?hello_word$"
		if 'Fuck' in req.headers or 'fuck' in req.headers:
			if search(regexp,req.headers['fuck'],I):
				plus('This site is vulnerabile to Cross Site Tracing (XST) at: %s'%(req.url))
