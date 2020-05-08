#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

import os

def dirs(path):
	files = []
	_ = os.listdir(path)
	for file in _:
		if not file.endswith('.py') or file == '__init__.py':pass
		else:files.append(file)
	return files