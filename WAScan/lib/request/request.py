#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

import ssl
import socket
import urllib2
from lib.utils.printer import *

if hasattr(ssl, '_create_unverified_context'): 
    ssl._create_default_https_context = ssl._create_unverified_context

def BasicAuthCredentials(creds):
	# return tuple
	return tuple(
		creds.split(':')
		)

def ProxyDict(proxy):
	# return dict
	return {
		'http'  : proxy,
		'https' : proxy
	}

class Request(object):
	"""docstring for Request"""
	def __init__(self,*kwargs):
		self.kwargs = kwargs
	
	def Send(self,url,method="get",data=None,headers=None):
		# make a request
		_dict_ = self.kwargs[0] # self.kwargs is a tuple, select [0]
		auth = None if "auth" not in _dict_ else _dict_["auth"]
		agent = None if "agent" not in _dict_ else _dict_["agent"]
		proxy = None if "proxy" not in _dict_ else _dict_["proxy"]
		pauth = None if "pauth" not in _dict_ else _dict_["pauth"]
		cookie = None if "cookie" not in _dict_ else _dict_["cookie"]
		timeout = None if "timeout" not in _dict_ else _dict_["timeout"]
		redirect = True if "redirect" not in _dict_ else _dict_["redirect"]
		_headers_ = None if "headers" not in _dict_ else _dict_["headers"]
		_data_ = None if "data" not in _dict_ else _dict_["data"]
		_method_ = None if "method"  not in _dict_ else _dict_["method"]
		# set method
		if method:
			if _method_ != None:
				method = _method_.upper()
			else:
				method = method.upper()
		# set data
		if data is None:
			if _data_ != None:
				data = _data_
			else:
				data = {}
		# if headers == None: headers = {}
		if headers is None: headers = {}
		# if auth == None: auth = () 
		if auth is None: auth = ()
		# set request headers
		# add user-agent header value
		if 'User-Agent' not in headers:
			headers['User-Agent'] = agent
		# _headers_ add to headers
		if isinstance(_headers_,dict):
			headers.update(_headers_)
		# process basic authentication
		if auth != None and auth != ():
			if ':' in  auth:
				authorization = ("%s:%s"%(BasicAuthCredentials(auth))).encode('base64')
				headers['Authorization'] = "Basic %s"%(authorization.replace('\n',''))
		# process proxy basic authorization
		if pauth != None:
			if ':' in pauth:
				proxy_authorization = ("%s:%s"%(BasicAuthCredentials(pauth))).encode('base64')
				headers['Proxy-authorization'] = "Basic %s"%(proxy_authorization.replace('\n',''))
		# process socket timeout
		if timeout != None:
			socket.setdefaulttimeout(timeout)
		# set handlers
		# handled http and https 
		handlers = [urllib2.HTTPHandler(),urllib2.HTTPSHandler()]
		# process cookie handler
		if 'Cookie' not in headers:
			if cookie != None and cookie != "":
				headers['Cookie'] = cookie
			# handlers.append(HTTPCookieProcessor(cookie))
		# process redirect
		if redirect != True:
			handlers.append(NoRedirectHandler)
		# process proxies
		if proxy:
			proxies = ProxyDict(proxy)
			handlers.append(urllib2.ProxyHandler(proxies))
		# install opener
		opener = urllib2.build_opener(*handlers)
		urllib2.install_opener(opener)
		# process method
		# method get 
		if method == "GET":
			if data: url = "%s?%s"%(url,data)
			req = urllib2.Request(url,headers=headers)
		# other methods
		elif method == "POST":
			req = urllib2.Request(url,data=data,headers=headers)
		# other methods
		else:
			req = urllib2.Request(url,headers=headers)
			req.get_method = lambda : method
		# response object
		try:
			resp = urllib2.urlopen(req)
		except urllib2.HTTPError,e:			
			resp = e
		except socket.error,e:
			exit(warn('Error: %s'%e))
		except urllib2.URLError,e:
			exit(warn('Error: %s'%e))
		return ResponseObject(resp)

class NoRedirectHandler(urllib2.HTTPRedirectHandler):
	"""docstring for NoRedirectHandler"""
	def http_error_302(self,req,fp,code,msg,headers):
		pass
	#  http status code 302
	http_error_302 = http_error_302 = http_error_302 = http_error_302

class ResponseObject(object):
	"""docstring for ResponseObject"""
	def __init__(self,resp):
		# get content
		self.content = resp.read()
		# get url 
		self.url = resp.geturl()
		# get status code
		self.code = resp.getcode()
		# get headers
		self.headers = resp.headers.dict