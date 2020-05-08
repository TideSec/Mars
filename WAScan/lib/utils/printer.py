#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from lib.utils.colors import *
from lib.utils.unicode import *

global logfile

global finger_dict



def setlog(log):
    global logfile

    logfile = log
    print "logfile:", logfile

def plus(string, name='test', flag="[+]"):
    global logfile
    log_file = open(logfile, 'a+')
    # print "string", string
    # print "name", name
    log_file.write(string + '^' + name + '\n')
    log_file.close()

    print "{}{}{} {}{}{}".format(
        GREEN % (0), flag, RESET,
        WHITE % (0), ucode(string), RESET
    )


def less(string, flag="[-]"):
    print "{}{}{} {}{}{}".format(
        RED % (0), flag, RESET,
        WHITE % (0), ucode(string), RESET
    )


def warn(string, flag="[!]"):
    print "{}{}{} {}{}{}".format(
        RED % (0), flag, RESET,
        RED % (0), ucode(string), RESET
    )


def test(string, flag="[*]"):
    print "{}{}{} {}{}{}".format(
        BLUE % (0), flag, RESET,
        WHITE % (0), ucode(string), RESET
    )


def info(string, flag="[i]"):
    print "{}{}{} {}{}{}".format(
        YELLOW % (0), flag, RESET,
        WHITE % (0), ucode(string), RESET
    )


def more(string, flag="|"):
    print " {}{}{}  {}{}{}".format(
        WHITE % (0), flag, RESET,
        WHITE % (0), ucode(string), RESET
    )


def null():
    print ""
