#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import findall,search,I
from lib.utils.printer import *

class cookies:
	def __run__(self,cookie):
		secure(cookie)
		httponly(cookie)
		domain(cookie)
		path(cookie)
		multiple(cookie)

def secure(cookie):
	if not search(r'secure;',cookie,I):
		# plus('Cookie without Secure flag set')
		pass

def httponly(cookie):
	if not search(r'httponly;',cookie,I):
		# plus('Cookie without HttpOnly flag set')
		pass

def domain(cookie):
	if search(r'domain\=\S*',cookie,I):
		domain = findall(r'domain\=(.+?);',cookie,I)
		if domain:
			# plus('Session Cookie are valid only at Sub/Domain: %s'%domain[0])
			pass
def path(cookie):
	if search(r'path\=\S*',cookie,I):
		path = findall(r'path\=(.+?);',cookie,I)
		if path:
			# plus('Session Cookie are valid only on that Path: %s'%path[0])
			pass

def multiple(cookie):
	if search(r'(.+?)\=\S*;',cookie,I):
		cookie_sessions = findall(r'(.+?)\=\S*;',cookie,I)
		for cs in cookie_sessions:
			if cs not in ['domain','path','expires']:
				# plus('Cookie Header contains multiple cookies')
				pass
				break