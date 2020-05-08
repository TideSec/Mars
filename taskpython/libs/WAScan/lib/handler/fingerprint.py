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
from lib.utils.printer import *
from lib.request.request import *
from importlib import import_module
from plugins.fingerprint.header.cookies import *
from plugins.fingerprint.header.header import *
from plugins.fingerprint.server.server import *

# -- global path
# print os.path.abspath('.')
# g_path = os.path.join(os.path.abspath('.').split('lib/')[0],'plugins/fingerprint/')
g_path = os.path.join(os.path.abspath('.').split('lib/')[0],'libs/WAScan/plugins/fingerprint/')

def Cms(headers,content):
	cms = []
	path = g_path+'cms/'
	# print path
	for file in dirs(path):
		file = file.split('.py')[0]
		__import__('plugins.fingerprint.cms.%s'%(file))
		module = sys.modules['plugins.fingerprint.cms.%s'%(file)]
		module = module.__dict__[file]
		cms.append(module(headers,content))
	return cms

def Framework(headers,content):
	framework = []
	path = g_path+'framework/'
	for file in dirs(path):
		file = file.split('.py')[0]
		__import__('plugins.fingerprint.framework.%s'%(file))
		module = sys.modules['plugins.fingerprint.framework.%s'%(file)]
		module = module.__dict__[file]
		framework.append(module(headers,content))
	return framework

def Language(content):
	language = []
	path =  g_path+'language/'
	for file in dirs(path):
		file = file.split('.py')[0]
		__import__('plugins.fingerprint.language.%s'%(file))
		module = sys.modules['plugins.fingerprint.language.%s'%(file)]
		module = module.__dict__[file]
		language.append(module(content))
	return language

def Os(headers):
	operating_system = []
	path = g_path+'os/'
	for file in dirs(path):
		file = file.split('.py')[0]
		__import__('plugins.fingerprint.os.%s'%(file))
		module = sys.modules['plugins.fingerprint.os.%s'%(file)]
		module = module.__dict__[file]
		operating_system.append(module(headers))
	return operating_system

def Waf(headers,content):
	web_app_firewall = []
	path = g_path+'waf/'
	for file in dirs(path):
		file = file.split('.py')[0]
		__import__('plugins.fingerprint.waf.%s'%(file))
		module = sys.modules['plugins.fingerprint.waf.%s'%(file)]
		module = module.__dict__[file]
		web_app_firewall.append(module(headers,content))
	return web_app_firewall

def Headers(headers,content):
	if 'set-cookie' in headers.keys() or 'cookie' in headers.keys():
		cookies().__run__(headers['set-cookie'] or headers['cookie'])
	header().__run__(headers)


class Fingerprint(Request):
	"""Fingerprint"""
	def __init__(self,kwargs,url):
		Request.__init__(self,kwargs)
		self.kwarg = kwargs
		self.url = url

	def run(self):
		info('Starting fingerprint target...')
		try:
			# -- request --
			req = self.Send(url=self.url,method="GET")
			# -- detect server --
			__server__ = server(self.kwarg,self.url).run()
			if __server__:
				# plus('Server: %s'%(__server__),'Server')
				plus('httpserver','%s'%(__server__))
			# -- detect cms
			__cms__ = Cms(req.headers,req.content)
			for cms in __cms__:
				if cms != (None and ""):
					plus('cms','%s'%(cms))
			# -- detect framework
			__framework__ = Framework(req.headers,req.content)
			for framework in __framework__:
				if framework != (None and ""):
					plus('Framework','%s'%(framework))
			# -- detect lang
			__lang__ = Language(req.content)
			for lang in __lang__:
				if lang != (None and ""):
					plus('Language','%s'%(lang))
			# -- detect os
			__os__ = Os(req.headers)
			for os in __os__:
				if os != (None and ""):
					plus('os_info','%s'%os)
			# -- detect waf
			__waf__ = Waf(req.headers,req.content)
			for waf in __waf__:
				if waf != (None and ""):
					plus('waf','%s'%waf)
			# Headers(req.headers,req.content)
		except Exception as e:
			print e
			pass