#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from urllib2 import HTTPError

class WascanUnboundLocalError(UnboundLocalError):
	pass

class WascanDataException(Exception):
	pass

class WascanNoneException(Exception):
	pass

class WascanInputException(Exception):
	pass

class WascanGenericException(Exception):
	pass

class WascanConnectionException(HTTPError):
	pass

class WascanKeyboardInterrupt(KeyboardInterrupt):
	pass