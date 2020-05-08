#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

import re
import string
from lib.parser.getcc import * 
from lib.parser.getmail import *
from lib.parser.getip import *
from lib.parser.getssn import *

class parse:
	def __init__(self,content):
		self.content = content 

	def clean(self):
		"""Clean HTML Response"""
		self.content = re.sub('<em>','',self.content)
		self.content = re.sub('<b>','',self.content)
		self.content = re.sub('</b>','',self.content)
		self.content = re.sub('<strong>','',self.content)
		self.content = re.sub('</strong>','',self.content)
		self.content = re.sub('</em>','',self.content)
		self.content = re.sub('<wbr>','',self.content)
		self.content = re.sub('</wbr>','',self.content)
		self.content = re.sub('<li>','',self.content)
		self.content = re.sub('</li>','',self.content)
		for x in ('>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C'):
			self.content = string.replace(self.content,x,' ')
	
	def getmail(self):
		"""Get Emails"""
		self.clean()
		return getmail(self.content)

	def getip(self):
		""" Get IP """
		self.clean()
		return getip(self.content)

	def getcc(self):
		""" Get Credit Card"""
		self.clean()
		return getcc(self.content)

	def getssn(self):
		""" """
		self.clean()
		return getssn(self.content)