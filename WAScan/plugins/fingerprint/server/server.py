#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from lib.request.request import *
from lib.utils.rand import *

class server(Request): 
	def __init__(self,kwargs,url):
		Request.__init__(self,kwargs)
		self.url = url

	def run(self):
		server = ""
		try:
			resp = self.Send(url=self.url,method="GET",headers={r_string(5) : r_string(10)})
			for item in resp.headers.items():
				if item[0].lower() == "server":
					server += item[1]
					break
			return server
		except Exception,e:
			pass