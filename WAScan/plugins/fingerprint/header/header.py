#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import findall,search,I
from lib.utils.printer import *

class header:
	def __run__(self,header):
		x_xss(header)
		x_frame(header)
		content_type(header)
		sts(header)
		x_content(header)
		uncommon(header)

def x_xss(headers):
	if 'x-xss-protection' not in headers.keys():
		info('X-XSS-Protection header missing')

def x_frame(headers):
	if 'x-frame-options' not in headers.keys():
		info('Clickjacking: X-Frame-Options header missing')

def content_type(headers):
	if 'content-type' not in headers.keys():
		info('Content-Type header missing')

def sts(headers):
	if 'strict-transport-security' not in headers.keys():
		info('Strict-Transport-Security header missing')

def x_content(headers):
	if 'x-content-type-options' not in headers.keys():
		info('X-Content-Type-Options header missing')

def uncommon(headers):
	common_header = ("server","age","cookie","pragma","accept","allow",
					"authorization","connection","cache-control","date","etag",
					"expires","expect","from","via","location","host","keep-live",
					"if-match","p3p","proxy-authenticate","proxy-authorization","range",
					"referer","set-cookie","te","trailer","vary","warning","www-authenticate",
					"x-powered-by","powered-by","x-pad","mime-version","proxy-connection","status",
					"public","dav","nncoection","dasl","x-aspbet-version","whisker","user-agent","upgrade",
					"transfer-encoding","retry-after","max-forwards","last-modified","if-range","if-none-match",
					"if-modified-since","if-unmodified-since","content-type","content-range","content-md5","content-location",
					"content-language","link","content-encoding","content-length","accept-charset","accept-encoding","accept-language","accept-ranges")
	for i in range(len(headers.keys())):
		if headers.keys()[i] not in common_header:
			info('Uncommon header \"%s\" found, with contents: %s'%(headers.keys()[i],headers[headers.keys()[i]]))