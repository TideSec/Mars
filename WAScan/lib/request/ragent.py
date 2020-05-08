#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from os import path
from random import randint
from lib.utils.readfile import *

def ragent():
	"""random agent"""
	user_agents = ()
	realpath = path.join(path.realpath(__file__).split('lib')[0],'lib/db/')
	realpath += "useragent.wascan"
	for _ in readfile(realpath):
		user_agents += (_,)
	return user_agents[randint(0,len(user_agents)-1)]