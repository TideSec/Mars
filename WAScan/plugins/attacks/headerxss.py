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
from lib.utils.payload import pxss

class headerxss(Request):
	""" Cross-Site Scripting (XSS) in headers value """
	get = "GET"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 
		self.data = data

	def run(self):
		"""Run"""
		info('Checking XSS on Headers..')
		self.cookie()
		self.referer()
		self.useragent()

	def cookie(self):
		""" Check cookie """
		for payload in pxss():
			headers = {
						'Cookie':'{}'.format(payload)
			}
			req = self.Send(url=self.url,method=self.get,headers=headers)
			# search payload in content
			if search(payload,req.content):
				plus("A potential \"Cross-Site Scripting (XSS)\" was found at cookie header value:")
				more("URL: {}".format(req.url))
				more("PAYLOAD: {}".format(payload))

	def referer(self):
		""" Check referer """
		for payload in pxss():
			headers = {
						'Referer':'{}'.format(payload)
			}
			req = self.Send(url=self.url,method=self.get,headers=headers)
			# search payload in content
			if search(payload,req.content):
				plus("A potential \"Cross-Site Scripting (XSS)\" was found at referer header value:")
				more("URL: {}".format(req.url))
				more("PAYLOAD: {}".format(payload))

	def useragent(self):
		""" Check user-agent """
		for payload in pxss():
			headers = {
						'User-Agent':'{}'.format(payload)
			}
			req = self.Send(url=self.url,method=self.get,headers=headers)
			# search payload in content
			if search(payload,req.content):
				plus("A potential \"Cross-Site Scripting (XSS)\" was found at user-agent header value:")
				more("URL: {}".format(req.url))
				more("PAYLOAD: {}".format(payload))