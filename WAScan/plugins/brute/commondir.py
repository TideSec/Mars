#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from os import path
from re import search, I
from Queue import Queue
from threading import Thread
from lib.utils.check import *
from lib.utils.printer import *
from lib.utils.readfile import *
from lib.request.request import *
from lib.utils.settings import MAX
from exceptions import *


def listing(resp):
    """ Listing """
    _ = False
    _ |= search(r'\<title\>Index of \/', resp, I) is not None
    _ |= search(r'\<a href\=\"?C\=N\;O\=D"\>Name\<\/a\>', resp, I) is not None
    _ |= search(r'\<A HREF\=\"?M\=A\"\>Last modified\<\/A\>', resp, I) is not None
    _ |= search(r'Last modified\<\/a\>', resp, I) is not None
    _ |= search(r'Parent Directory\<\/a\>', resp, I) is not None
    _ |= search(r'\<TITLE\>Folder Listing.', resp, I) is not None
    _ |= search(r'\<table summary\=\"Directory Listing', resp, I) is not None
    _ |= search(r'\"\>[To Parent Directory]\<\/a\>\<br\>\<br\>', resp, I) is not None
    return _


class commondir(Request):
    """ Common Direcotories """
    get = "GET"

    def __init__(self, kwargs, url, data):
        Request.__init__(self, kwargs)
        self.url = url 
        self.data = data

    def run(self):
        plus('Bruteforce common dirs...')
        # set queue to MAX queues
        queue = Queue(MAX)
        for _ in xrange(MAX):
            # call ThreadBrute class
            thread = ThreadBrute(self.url, queue, self)
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
        realpath = path.join(path.realpath(__file__).split('plugins')[0],
                             "lib/db/")
        return (realpath + "commondir.wascan")


class ThreadBrute(Thread):
    """ Bruteforcer """
    get = "GET"

    def __init__(self, target, queue, request):
        Thread.__init__(self)
        self.queue = queue
        self.target = target
        self.request = request

    def run(self):
        while True:
            try:
                # if self.queue.full() == False: exit()
                # if self.queue.empty() == True: exit()
                path = self.queue.get()
                # check url path
                url = CPath(self.target, path)
                # send request
                req = self.request.Send(url=url, method=self.get)
                # if status code == 200
                if req.code == 200:
                    # and req.url == url
                    if CEndUrl(req.url) == url:
                        plus('A potential \"{}\" directory '
                             'was found at: {}'
                             .format(path, req.url))
                        # check listing enabled
                        if listing(req.content):
                            more('Listing enabled for this directory')
                # done queue task
                self.queue.task_done()
            except Exception, e:
                pass
            except AttributeError, e:
                pass
            except TypeError, e:
                pass
