#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from re import search,I 

def magento(headers,content):
	_  = False
	if 'set-cookie' in headers.keys():
		_ |= search(r"magento=[0-9a-f]+|frontend=[0-9a-z]+",headers["set-cookie"],I) is not None
	_ |= search(r"images/logo.gif\" alt\=\"Magento Commerce\" \/\>\<\/a\>\<\/h1\>",content) is not None
	_ |= search(r"\<a href\=\"http://www.magentocommerce.com/bug-tracking\" id\=\"bug_tracking_link\"\>\<strong\>Report All Bugs\<\/strong\>\<\/a\>",content) is not None
	_ |= search(r"\<link rel\=\"stylesheet\" type\=\"text/css\" href\=\"[^\"]+\/skin\/frontend\/[^\"]+\/css\/boxes.css\" media\=\"all\"",content) is not None
	_ |= search(r"\<div id\=\"noscript-notice\" class\=\"magento-notice\"\>",content) is not None
	_ |= search(r"Magento is a trademark of Magento Inc. Copyright &copy; ([0-9]{4}) Magento Inc",content) is not None
 	if _ : return "Magento"