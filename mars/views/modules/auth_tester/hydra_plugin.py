#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-6-19
# @File    : hydra_plugin.py
# @Desc    : ""

import os
import signal
import shlex
import random
import string
import re
from datetime import datetime
from subprocess import PIPE, Popen


class HydraScanner:

    def __init__(self, target_list, service, username_list, password_list, args):
        self.target_list = target_list
        self.service = service
        self.username_list = username_list
        self.password_list = password_list
        self.args = args
        self.dict_path = '/tmp/hydra_dict_' + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.target_path = '/tmp/hydra_target_' + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.stdout = ''
        self.stderr = ''
        self.result = []

    def scanner(self):
        command = self._format_args()
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        try:
            (self.stdout, self.stderr) = process.communicate()
            # print self.stdout
        except Exception as e:
            print(process.pid, e)
        if os.path.exists(self.dict_path):
            os.remove(self.dict_path)
        if os.path.exists(self.target_path):
            os.remove(self.target_path)
        return self._format_res()

    def _format_args(self):
        # list of servers to attack, one entry per line, ':' to specify port
        with open(self.target_path, 'w') as target_file:
            for target in self.target_list:
                target_file.write(target + "\n")
        # The redis, cisco, oracle-listener, s7-300, snmp and vnc modules
        # are only using the -p or -P option, not login (-l, -L) or colon file (-C)
        if self.service in ['redis', 'cisco', 'oracle-listener', 's7-300', 'snmp', 'vnc']:
            with open(self.dict_path, 'w') as dict_file:
                for password in self.password_list:
                    dict_file.write(password + "\n")
            command = 'hydra -w 15 %s -P %s -M %s %s' % (self.args, self.dict_path, self.target_path, self.service)
        else:
            # colon separated "login:pass" format, instead of -L/-P options
            with open(self.dict_path, 'w') as dict_file:
                for username in self.username_list:
                    for password in self.password_list:
                        dict_file.write(username + ":" + password + "\n")
            command = 'hydra -w 15 %s -C %s -M %s %s' % (self.args, self.dict_path, self.target_path, self.service)
            # hydra -C /tmp/hydra_dict_84V9H6hx -M /tmp/hydra_target_cIjX1prQ redis
        # print command
        return shlex.split(command)

    def _format_res(self):
        result_list = []
        result = {}
        pattern_res = '(\[\d+\]\[%s\]\shost:\s\d+\.\d+\.\d+\.\d+.*?)\n' % self.service
        pattern_host = 'host:\s(\d+\.\d+\.\d+\.\d+)\s'
        pattern_username = 'login:\s(.+?)\s+password:'
        pattern_password = 'password:\s(.+?)$'
        re_result = re.findall(pattern_res, self.stdout)
        for res in re_result:
            try:
                if re.findall(pattern_host, res):
                    host = re.findall(pattern_host, res)[0]
                else:
                    host = 'None'
                if re.findall(pattern_username, res):
                    username = re.findall(pattern_username, res)[0]
                else:
                    username = "None"
                if re.findall(pattern_password, res):
                    password = re.findall(pattern_password, res)[0]
                else:
                    password = "None"
                result['target'] = host
                result['service'] = self.service
                result['username'] = username
                result['password'] = password
                result_list.append(result)
                result = {}
            except Exception as e:
                print(res, e)
        return result_list


class ServiceCheck:

    def __init__(self, target, service, args):
        self.target = target
        self.service = service
        self.args = args
        self.username = 'None'
        self.password = 'None'
        self.stdout = ''
        self.stderr = ''
        self.flag_list = [
            'Anonymous success',
            'not require password'
        ]

    def service_check(self):
        # print("[*] Service Check %s %s" % (self.target, self.service))
        command = self._format_args()
        start_time = datetime.now()
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        try:
            while process.poll() is None:
                now_time = datetime.now()
                if (now_time - start_time).seconds > 15:
                    try:
                        os.kill(process.pid, signal.SIGTERM)
                    except OSError as e:
                        print(process.pid, e)
                    return False
            (self.stdout, self.stderr) = process.communicate()
        except Exception as e:
            print(process.pid, e)
        return self.host_check()

    def _format_args(self):
        if self.service in ['redis', 'cisco', 'oracle-listener', 's7-300', 'snmp', 'vnc']:
            # hydra -w 30 -p 123456 redis://192.168.1.1
            command = 'hydra -w 30 %s -p %s %s://%s' % (self.args, self.password, self.service, self.target)
        else:
            # hydra -w 30 -l root -p 123456 mysql://192.168.1.1
            command = 'hydra -w 30 %s -l %s -p %s %s://%s' % (self.args, self.username, self.password,
                                                              self.service, self.target)
        return shlex.split(command)

    def host_check(self):
        for flag in self.flag_list:
            if flag in self.stderr:
                return {"target": self.target, "result": {'username': self.username, "password": self.password}}
        if "successfully" in self.stdout and self.target in self.stdout:
            return {"target": self.target, "result": {'username': self.username, "password": self.password}}
        elif 'can not connect' in self.stderr:
            return False
        elif 'waiting for children to finish' in self.stdout:
            return False
        else:
            return {"target": self.target, "result": ""}
