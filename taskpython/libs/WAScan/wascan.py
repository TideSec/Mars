#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# --
import sys
import getopt
# -- lib
from lib.utils.printer import *
from lib.utils.usage import *
from lib.utils.check import *
from lib.utils.settings import *
from lib.request.ragent import *
from lib.utils.exception import *
# -- modules
from lib.handler.audit import *
from lib.handler.brute import *
from lib.handler.attacks import *
from lib.handler.crawler import *
from lib.handler.fullscan import *
from lib.handler.disclosure import *
from lib.handler.fingerprint import *


class wascan(object):
    """ WAScan """
    usage = usage()

    def main(self):
        kwargs = ARGS
        # verbose default == False
        verbose = False
        # scan default == 5
        scan = "5"
        if len(sys.argv) < 2:
            # True == exit
            self.usage.basic(True)
        try:
            opts, args = getopt.getopt(ARGV[1:], CHAR, LIST_NAME)
        except getopt.GetoptError, e:
            # True == exit
            print e
            self.usage.basic(True)
        # wascan banner
        # self.usage.banner()
        outlog = ''
        url = ''
        # process args
        for opt, arg in opts:
            if opt in ('-u', '--url'): url = CUrl(arg)
            if opt in ('-s', '--scan'): scan = CScan(arg)
            if opt in ('-H', '--headers'): kwargs['headers'] = CHeaders(arg)
            if opt in ('-d', '--data'): kwargs['data'] = arg
            if opt in ('-b', '--brute'): kwargs['brute'] = True
            if opt in ('-m', '--method'): kwargs['method'] = arg
            if opt in ('-h', '--host'): kwargs['headers'].update({'Host': arg})
            if opt in ('-R', '--referer'): kwargs['headers'].update({'Referer': arg})
            if opt in ('-a', '--auth'): kwargs['auth'] = CAuth(arg)
            if opt in ('-A', '--agent'): kwargs['agent'] = arg
            if opt in ('-C', '--cookie'): kwargs['cookie'] = arg
            if opt in ('-r', '--ragent'): kwargs['agent'] = ragent()
            if opt in ('-p', '--proxy'): kwargs['proxy'] = arg
            if opt in ('-P', '--proxy-auth'): kwargs['pauth'] = CAuth(arg)
            if opt in ('-t', '--timeout'): kwargs['timeout'] = float(arg)
            if opt in ('-n', '--redirect'): kwargs['redirect'] = False
            if opt in ('-v', '--verbose'): verbose = True
            if opt in ('-V', '--version'): version = Version()
            if opt in ('-hh', '--help'): self.usage.basic(True)
            if opt in ('-o', '--out'): outlog = arg
        # starting
        parse = SplitURL(url)
        try:
            if outlog:
                setlog(outlog)
            PTIME(url)

            # if kwargs['brute']:
            #     BruteParams(kwargs, url, kwargs['data']).run()
            if scan == 0:
                Fingerprint(kwargs, url).run()
            if scan == 1:
                Attacks(kwargs, url, kwargs['data'])
            if scan == 2:
                Audit(kwargs, url, kwargs['data'])
            if scan == 3:
                Brute(kwargs, url, kwargs['data'])
            if scan == 4:
                Disclosure(kwargs, url, kwargs['data']).run()
            # full scan
            if int(scan) == 5:
                info('Starting full scan module...')
                Fingerprint(kwargs, url).run()
                for u in Crawler().run(kwargs, url, kwargs['data']):
                    test('Testing URL: %s' % (u))
                    if '?' not in url:
                        warn('Not found query in this URL... Skipping..')
                    if type(u[0]) is tuple:
                        kwargs['data'] = u[1]
                        FullScan(kwargs, u[0], kwargs['data'])
                    else:
                        FullScan(kwargs, u, kwargs['data'])
                Audit(kwargs, parse.netloc, kwargs['data'])
                Brute(kwargs, parse.netloc, kwargs['data'])
        except WascanUnboundLocalError, e:
            pass


if __name__ == "__main__":
    try:
        wascan().main()
    except KeyboardInterrupt, e:
        exit(warn('Exiting... :('))
