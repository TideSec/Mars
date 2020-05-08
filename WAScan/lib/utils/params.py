#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import sub,I

class preplace:
	""" replace params with payload"""
	def __init__(self,url,payload,data):
		self.url = url 
		self.data = data
		self._params = []
		self.payload = payload

	def get(self):
		"""get"""
		params = self.url.split("?")[1].split("&")
		for param in params:
			ppayload = param.replace(param.split("=")[1],self.payload)
			porignal = param.replace(ppayload.split("=")[1],param.split("=")[1])
			self._params.append(sub(porignal,ppayload,self.url))

	def post(self):
		"""post"""
		params = self.data.split("&")
		for param in params:
			ppayload = param.replace(param.split("=")[1],self.payload)
			porignal = param.replace(ppayload.split("=")[1],param.split("=")[1])
			self._params.append(self.data.replace(porignal,ppayload))

	def run(self):
		if "?" in self.url and self.data == None:
			self.get()
		elif "?" not in self.url and self.data != None:
			self.post()
		else:
			self.get()
			self.post()
		return self._params

class padd:
	""" add the payload to params """
	def __init__(self,url,payload,data):
		self.url = url 
		self.data = data
		self._params = []
		self.payload = payload

	def get(self):
		"""get"""
		params = self.url.split("?")[1].split("&")
		for param in params:
			ppayload = param.replace(param.split("=")[1],param.split('=')[1]+self.payload)
			porignal = param.replace(ppayload.split("=")[1],param.split("=")[1])
			self._params.append(sub(porignal,ppayload,self.url))

	def post(self):
		"""post"""
		params = self.data.split("&")
		for param in params:
			ppayload = param.replace(param.split("=")[1],param.split('=')[1]+self.payload)
			porignal = param.replace(ppayload.split("=")[1],param.split("=")[1])
			self._params.append(self.data.replace(porignal,ppayload))

	def run(self):
		if "?" in self.url and self.data == None:
			self.get()
		elif "?" not in self.url and self.data != None:
			self.post()
		else:
			self.get()
			self.post()
		return self._params