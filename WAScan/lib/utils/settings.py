#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from sys import argv
from time import strftime
from lib.request.ragent import *
from lib.utils.printer import *


# tool name
NAME = argv[0]

# tool version
VERSION = "v0.2.1"

# author
AUTHOR = "Momo Outaadi (M4ll0k)"

# description
DESCRIPTION = "Web Application Scanner"

# name + description + version
NVD = (NAME.split('.')[0]).title()+": "+DESCRIPTION+" - "+VERSION

# max threads
MAX = 5

# args
CHAR = "u:s:H:d:m:h:R:a:A:c:p:P:t:o:n:v=:V=:r=:b=:"

LIST_NAME = [
    "url=",
    "scan=",
    "headers=",
    "data=",
    "method=",
    "host=",
    "referer=",
    "auth=",
    "agent=",
    "cookie=",
    "proxy=",
    "proxy-auth=",
    "timeout=",
    "outlog="
    "redirect",
    "verbose",
    "brute",
    "ragent",
    "version",
    "help"
]

# argv
ARGV = argv
# dict args
ARGS = {
    'auth': None,
    'brute': None,
    'agent': ragent(),
    'proxy': None,
    'pauth': None,
    'cookie': None,
    'timeout': 5,
    'redirect': True,
    'headers': {},
    'data': None,
    'method': 'GET'
}

# time
TIME = strftime('%d/%m/%Y at %H:%M:%S')
TNOW = strftime('%H:%M:%S')


# print version
def Version():
    print "\n{}".format(NVD)
    print "Author: {}\n".format(AUTHOR)
    exit()


# print time and url
def PTIME(url):
    # plus("URL: {}".format(url))
    # plus("Starting: {}".format(TIME))
    null()
