#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from os import path
from json import loads
from re import search,I 
from lib.utils.params import *
from lib.utils.printer import *
from lib.utils.readfile import *
from lib.request.request import *
from lib.utils.payload import xpath

class xpathi(Request):
	""" XPath Injection """
	get = "GET"
	post = "POST"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 
		self.data = data

	def serror(self,resp):
		""" Return error """
		_ = None
		realpath = path.join(path.realpath(__file__).split('plugins')[0],'lib/db/errors')
		abspath = realpath+"/"+"xpath.json"
		_ = self.search(resp,loads(readfile(abspath)[0],encoding="utf-8"))
		if _ != None: return _

	def search(self,resp,content):
		""" Search error in response """
		for error in content['info']['regexp']:
			if search(error,resp):
				_ = content['info']['name']
				return _

	def run(self):
		""" Run """
		info('Checking XPath Injection...')
		URL = None
		DATA = None
		PAYLOAD = None
		for payload in xpath():
			# post method
			if self.data:
				# data add payload
				rPayload = padd(self.url,payload,self.data)
				for data in rPayload.run():
					# send request
					req = self.Send(url=self.url,method=self.post,data=data)
					# search error
					error = self.serror(req.content)
					if error:
						URL = req.url 
						DATA = data 
						PAYLOAD = payload
						break
			# get method
			else:
				# url query add payload
				urls = padd(self.url,payload,None)
				for url in urls.run():
						# send request 
						req = self.Send(url=url,method=self.get)
						# search error
						error = self.serror(req.content)
						if error:
							URL = url
							PAYLOAD = payload
							break
				# if URL and PAYLOAD not empty 
				if URL and PAYLOAD:
					# print 
					if DATA != None:
						plus("A potential \"XPath Injection\" was found at:")
						more("URL: {}".format(URL))
						more("POST DATA: {}".format(DATA))
						more("PAYLOAD: {}".format(PAYLOAD))
					elif DATA == None:
						plus("A potential \"XPath Injection\" was found at:")
						more("URL: {}".format(URL))
						more("PAYLOAD: {}".format(PAYLOAD))
					# break
					break
