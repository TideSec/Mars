#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from os import path
from re import search
from lib.utils.check import *
from lib.utils.printer import *
from lib.utils.readfile import *
from lib.request.request import *

class phpinfo(Request):
	""" phpinfo  """
	get = "GET"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 
		self.data = data

	def search(self):
		""" Search Path """
		_ = None
		realpath = path.join(path.realpath(__file__).split('plugins')[0],'lib/db/')
		return (realpath+"phpinfo.wascan")

	def run(self):
		""" Run """
		info('Checking PHPInfo...')
		for path in readfile(self.search()):
			# check url path
			url = CPath(self.url,path)
			# send request 
			req = self.Send(url=url,method=self.get,)
			# if status code == 200
			if req.code == 200:
				# and search in req.content
				if search(r'\<title\>phpinfo()\<\/title\>|\<h1 class\=\"p\"\>PHP Version',req.content):
					plus('Found phpinfo page at: %s'%(req.url))
					break