#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

import os
import sys
from lib.utils.dirs import *
from lib.request.request import *
from lib.utils.printer import *
from importlib import import_module
from plugins.brute.params import *

path = os.path.join(os.path.abspath('.').split('lib')[0],'plugins/disclosure/')

class Disclosure(Request):
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 

	def run(self):
		info('Starting disclosure module...')
		req = self.Send(url=self.url,method='GET')
		for file in dirs(path):
			file = file.split('.py')[0]
			__import__('plugins.disclosure.%s'%(file))
			module = sys.modules['plugins.disclosure.%s'%(file)]
			module = module.__dict__[file]
			if file == 'errors':module(req.content,req.url)
			else:module(req.content)