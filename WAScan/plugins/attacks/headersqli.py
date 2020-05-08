#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from json import loads
from re import search,I 
from os import path,listdir
from lib.utils.params import *
from lib.utils.printer import *
from lib.utils.readfile import *
from lib.request.request import *
from lib.utils.payload import sql

class headersqli(Request):
	""" SQL Injection via header values"""
	get = "GET"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 
		self.data = data

	def serror(self,resp):
		""" Return error """
		_ = None
		realpath = path.join(path.realpath(__file__).split('plugins')[0],'lib/db/sqldberror')
		for file in listdir(realpath):
			abspath = realpath+"/"+file
			_ = self.search(resp,loads(readfile(abspath)[0],encoding="utf-8"))
			if _ != None: return _

	def search(self,resp,content):
		""" Search error in response """
		for error in content['db']['regexp']:
			if search(error,resp):
				_ = content['db']['name']
				return _

	def run(self):
		""" Run """
		info('Checking SQL Injection on Headers...')
		self.cookie()
		self.referer()
		self.useragent()

	def cookie(self):
		""" check cookie header value """
		DB = None
		URL = None
		DATA = None
		PAYLOAD = None
		for payload in sql():
			# cookie header
			headers = {
						'Cookie':'{}'.format(payload)
						}
			req = self.Send(url=self.url,method=self.get,headers=headers)
			# search errors
			error = self.serror(req.content)
			if error:
				DB = error
				URL = req.url
				PAYLOAD = payload
				break
		# if URL and PAYLOAD not empty 
		if URL and PAYLOAD:
			plus("A potential \"SQL Injection\" was found at cookie header value:")
			more("URL: {}".format(URL))
			more("PAYLOAD: {}".format(PAYLOAD))
			more("DBMS: {}".format(DB))

	def referer(self):
		""" check referer header value """
		DB = None
		URL = None
		DATA = None
		PAYLOAD = None
		for payload in sql():
			# cookie header
			headers = {
						'Referer':'{}'.format(payload)
						}
			req = self.Send(url=self.url,method=self.get,headers=headers)
			# search errors
			error = self.serror(req.content)
			if error:
				DB = error
				URL = req.url
				PAYLOAD = payload
				break
		# if URL and PAYLOAD not empty 
		if URL and PAYLOAD:
			plus("A potential \"SQL Injection\" was found at referer header value:")
			more("URL: {}".format(URL))
			more("PAYLOAD: {}".format(PAYLOAD))
			more("DBMS: {}".format(DB))

	def useragent(self):
		""" check useragent header value """
		DB = None
		URL = None
		DATA = None
		PAYLOAD = None
		for payload in sql():
			# cookie header
			headers = {
						'User-Agent':'{}'.format(payload)
						}
			req = self.Send(url=self.url,method=self.get,headers=headers)
			# search errors
			error = self.serror(req.content)
			if error:
				DB = error
				URL = req.url
				PAYLOAD = payload
				break
		# if URL and PAYLOAD not empty 
		if URL and PAYLOAD:
			plus("A potential \"SQL Injection\" was found at user-agent header value:")
			more("URL: {}".format(URL))
			more("PAYLOAD: {}".format(PAYLOAD))
			more("DBMS: {}".format(DB))