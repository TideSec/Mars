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
from lib.utils.check import *
from lib.utils.rand import r_string
from lib.request.request import *
from lib.utils.payload import crlfp

class crlf(Request):
	""" Carriage Return Line Feed """
	get = "GET"
	post = "POST"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 
		self.data = data

	def run(self):
		""" Run """
		info('Checking CRLF Injection...')
		URL = None
		DATA = None
		PAYLOAD = None
		# start
		for payload in crlfp():
			random_string = r_string(20)
			payload = payload.replace('=injection',random_string)
			# check host 
			req = self.Send(CPath(self.url,'/%s'%payload),method=self.get)
			if 'Set-Cookie' in req.headers.keys():
				if search(random_string,req.headers['Set-Cookie'],I):
					plus('A potential \"Carriage Return Line Feed\" was found at: ')
					more('URL: {}'.format(req.url))
					more('PAYLOAD: {}'.format(payload))
					break
			# post method
			if self.data:
				# data add payload
				addPayload = preplace(self.url,payload,self.data)
				for data in addPayload.run():
					# send request
					req = self.Send(url=self.url,method=self.post,data=data)
					# search payload in response content
					if 'Set-Cookie' in req.headers.keys():
						if search(random_string,req.headers['Set-Cookie'],I):
							URL = req.url 
							DATA = data 
							PAYLOAD = payload
							break
			# get method
			else:
				# url and payload
				urls = preplace(self.url,payload,None)
				for url in urls.run():
					# send request
					req = self.Send(url=url,method=self.get)
					# search payload in response content
					if 'Set-Cookie' in req.headers.keys():
						if search(random_string,req.headers['Set-Cookie'],I):
							URL = url
							PAYLOAD = payload
							break
			# break if URL and PAYLOAD not empty
			if URL and PAYLOAD:
				# print
				if DATA != None:
					plus("A potential \"Carriage Return Line Feed\" was found at:")
					more("URL: {}".format(URL))
					more("POST DATA: {}".format(DATA))
					more("PAYLOAD: {}".format(PAYLOAD))
				elif DATA == None:
					plus("A potential \"Carriage Return Line Feed\" was found at:")
					more("URL: {}".format(URL))
					more("PAYLOAD: {}".format(PAYLOAD))
				# break
				break
			