#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from re import search,I
from lib.utils.params import *
from lib.utils.printer import *
from lib.request.request import *
from lib.utils.payload import ssip

class ssi(Request):
	""" Server Side Injection """
	get = "GET"
	post = "POST"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 
		self.data = data

	def run(self):
		""" Run """
		info('Checking Server Side Injection...')
		URL = None
		DATA = None
		PAYLOAD = None
		# start
		for payload in ssip():
			# post method
			if self.data:
				# data add payload
				addPayload = padd(self.url,payload,self.data)
				for data in addPayload.run():
					# send request
					req = self.Send(url=self.url,method=self.post,data=data)
					# search payload in response content
					if search(r'root:/bin/[bash|sh]',req.content):
						URL = req.url 
						DATA = data 
						PAYLOAD = payload
						break
			# get method
			else:
				# url and payload
				urls = padd(self.url,payload,None)
				for url in urls.run():
					# send request
					req = self.Send(url=url,method=self.get)
					# search payload in response content
					if search(r'root:/bin/[bash|sh]',req.content):
						URL = url
						PAYLOAD = payload
						break
			# break if URL and PAYLOAD not empty
			if URL and PAYLOAD:
				# print
				if DATA != None:
					plus("A potential \"Server Side Injection\" was found at:")
					more("URL: {}".format(URL))
					more("POST DATA: {}".format(DATA))
					more("PAYLOAD: {}".format(PAYLOAD))
				elif DATA == None:
					plus("A potential \"Server Side Injection\" was found at:")
					more("URL: {}".format(URL))
					more("PAYLOAD: {}".format(PAYLOAD))
				# break
				break
			