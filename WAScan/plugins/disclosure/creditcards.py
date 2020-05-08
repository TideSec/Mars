#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from lib.utils.printer import *
from lib.parser.parse import *

def creditcards(content):
	_list_ = parse(content).getcc()
	if _list_ != None or _list_ != []:
		if len(_list_) >= 2:
			plus('Credit card number disclosure: %s'%(str(_list_).split('[')[1].split(']')[0]))
		elif len(_list_) == 1:
			plus('Credit card number disclosure: %s'%_list_[0])