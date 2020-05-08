#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from lib.utils.printer import info
from lib.request.crawler import SCrawler

class Crawler:
    """ cralwer """
    def run(self, kwargs, url, data):
        info("Starting crawler...")
        links = []
        links.append(url)
        for link in links:
            for k in SCrawler(kwargs, url, data).run():
                if k not in links:
                    links.append(k)
        return links
