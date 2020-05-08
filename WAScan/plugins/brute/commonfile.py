#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from os import path
from Queue import Queue
from threading import Thread 
from lib.utils.check import *
from lib.utils.printer import *
from lib.utils.readfile import *
from lib.request.request import *
from lib.utils.settings import MAX
from exceptions import *

class commonfile(Request):
	""" Common Files """
	get = "GET"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 
		self.data = data

	def run(self):
		plus('Bruteforce common files...')
		# set queue to MAX queues
		queue = Queue(MAX)
		for _ in xrange(MAX):
			# call ThreadBrute class
			thread = ThreadBrute(self.url,queue,self)
			# set daemon 
			thread.daemon = True
			# starting thread
			thread.start()
		# reading file 
		for path in readfile(self.search()):
			queue.put(path)
		queue.join()

	def search(self):
		""" search data path """
		realpath = path.join(path.realpath(__file__).split('plugins')[0],"lib/db/")
		return (realpath + "commonfile.wascan")

class ThreadBrute(Thread):
	""" Bruteforcer """
	get = "GET"
	def __init__(self,target,queue,request):
		Thread.__init__(self)
		self.setDaemon = True
		self.queue = queue
		self.target = target
		self.request = request

	def run(self):
		while True:
			try:
				#if self.queue.full() == False: exit()
				#if self.queue.empty() == True: exit()
				# check url path
				url = CPath(self.target,self.queue.get())
				# send request
				req = self.request.Send(url=url,method=self.get)
				# if status code == 200
				if req.code == 200:
					# and req.url == url
					if CEndUrl(req.url) == url:
						plus('A potential file was found at: {}'.format(req.url))
				# done queue task)
				self.queue.task_done()
			except Exception,e:
				pass
			except AttributeError,e:
				pass
			except TypeError,e:
				pass