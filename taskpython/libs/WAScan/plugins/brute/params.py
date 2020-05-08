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
from lib.utils.settings import TNOW
from urllib2 import HTTPError

class params(Request):
	""" Search hidden params """
	get = "GET"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url
		self.data = data

	def run(self):
		exit(0)
		info('Bruteforce hidden params...')
		info('A potential hidden parameters searching...')
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
		return (realpath + "params.wascan")

class ThreadBrute(Thread):
	""" Bruteforcer """
	get = "GET"
	def __init__(self,target,queue,request):
		Thread.__init__(self)
		self.queue = queue
		self.target = target
		self.request = request

	def run(self):

		while True:
			try:
				req_1 = self.request.Send(url=self.target,method=self.get)
				# check if path exist on the server
				url = CQuery(req_1.url,self.queue.get())
				req_2 = self.request.Send(url=url,method=self.get)
				if req_2.code in range(200,399):
					if len(req_1.content) != len(req_2.content):
						more('[{}] [{}]'.format(req_2.code,CParams(req_2.url)))
				# done queue task
				self.queue.task_done()
			except Exception,e:
				pass
			except AttributeError,e:
				pass
			except TypeError,e:
				pass