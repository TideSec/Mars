#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from lib.utils.check import *
from lib.utils.printer import *
from lib.utils.unicode import *
from urllib import unquote_plus
from re import search,findall,I
from lib.request.request import *
from urlparse import urlsplit,urlunparse
import lxml
try:
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from bs4 import BeautifulSoup

EXCLUDED_MEDIA_EXTENSIONS = (
    '.7z', '.aac', '.aiff', '.au', '.avi', '.bin', '.bmp', '.cab', '.dll', '.dmp', '.ear', '.exe', '.flv', '.gif',
    '.gz', '.image', '.iso', '.jar', '.jpeg', '.jpg', '.mkv', '.mov', '.mp3', '.mp4', '.mpeg', '.mpg', '.pdf', '.png',
    '.ps', '.rar', '.scm', '.so', '.tar', '.tif', '.war', '.wav', '.wmv', '.zip'
)

class SCrawler(Request):
	""" Simple Crawler """
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 
		self.data = data
		self.forms = []
		self.ok_links = []
		self.all_links = []
		self.scheme = urlsplit(url).scheme
		self.netloc = urlsplit(url).netloc
		self.content = None

	def run(self):
		# send request
		resp = self.Send(url=self.url,data=self.data)
		self.content = resp.content
		self.extract 
		for link in self.all_links:
			r_link = self.absolute(link)
			if r_link:
				if r_link not in self.ok_links:
					self.ok_links.append(r_link)
		return self.ok_links

	@property
	def extract(self):
		# href
		for tag in self.soup.findAll('a',href=True):
			self.all_links.append(tag['href'].split('#')[0])
		# src
		for tag in self.soup.findAll(['frame','iframe'],src=True):
			self.all_links.append(tag['src'].split('#')[0])
		# formaction
		for tag in self.soup.findAll('button',formaction=True):
			self.all_links.append(tag['formaction'])
		# extract form 
		form = self.form()
		if form != None and form != []:
			if form not in self.all_links:
				self.all_links.append(form)

	@property
	def soup(self):
		soup = BeautifulSoup(self.content,"lxml")
		return soup

	def check_ext(self,link):
		"""check extension"""
		if link not in EXCLUDED_MEDIA_EXTENSIONS:
			return link

	def check_method(self,method):
		"""check method"""
		if method != []:
			return "GET"
		elif method != []:
			return method[0]

	def check_url(self,url):
		"""check url"""
		url = unquote_plus(url)
		url = url.replace("&amp;","&")
		url = url.replace("#","")
		url = url.replace(" ","+")
		return url 

	def check_action(self,action,url):
		""" check form action """
		if action == [] or action[0] == "/":
			return self.check_url(url)
		elif action != [] and action != "":
			if action[0] in url:
				self.check_url(url)
			else:
				return self.check_url(CPath(url+action[0]))

	def check_name_value(self,string):
		""" check form name and value """
		if string == []:
			return "TEST"
		elif string != []:
			return string[0]

	def form(self):
		""" search forms """
		for form in self.soup.findAll('form'):
			if form not in self.forms:
				self.forms.append(form)
		for form in self.forms:
			if form != "" and form != None:
				return self.extract_form(str(form),self.url)

	def extract_form(self,form,url):
		""" extract form """
		query = []
		action = ""
		method = ""
		try:
			# method
			method += self.check_method(findall(r'method=[\'\"](.+?)[\'\"]',form,I))
			# action
			action += self.check_action((findall(r'method=[\'\"](.+?)[\'\"]',form,I),url))
		except Exception,e:
			pass
		for inputs in form.split('/>'):
			if search(r'\<input',inputs,I):
				try:
					# name
					name = self.check_name_value(findall(r'name=[\'\"](.+?)[\'\"]',inputs,I))
					# value
					value = self.check_name_value(findall(r'value=[\'\"](.+?)[\'\"]',inputs,I))
					name_value = "%s=%s"%(name,value)
					if len(query) == 0:query.append(name_value)
					if len(query) == 1:query[0] += "&%s"%(name_value) 
				except Exception,e:
					pass
		if action:
			if method.lower() == "get":
				if query != []:
					return "%s?%s"%(action,query[0])
				return action
			elif method.lower() == "post":
				if query != []:
					return action,query[0]
				return action

	def absolute(self,link):
		""" make absolute url """
		link = self.check_ext(link)
		parts = urlsplit(link)
		# urlsplit 
		scheme = ucode(parts.scheme)
		netloc = ucode(parts.netloc)
		path = ucode(parts.path) or '/'
		query = ucode(parts.query)
		# make 
		if scheme == 'http' or scheme == 'https':
			if netloc != "":
				if netloc in self.netloc:
					return urlunparse((scheme,netloc,path,'',query,''))
		#
		elif link.startswith('//'):
			if netloc != "":
				if self.netloc in netloc:
					return urlunparse((self.scheme,netloc,(path or '/'),'',query,''))
		#
		elif link.startswith('/'):
			return urlunparse((self.scheme,self.netloc,path,'',query,''))
		#
		elif link.startswith('?'):
			return urlunparse((self.scheme,self.netloc,path,'',query,''))
		#
		elif link == "" or link.startswith('#'):
			return self.url 
		#
		else:
			return urlunparse((self.scheme,self.netloc,path,'',query,''))
