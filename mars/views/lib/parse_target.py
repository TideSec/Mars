#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-15
# @File    : parse_target.py
# @Desc    : ""

import ipaddr
import re


def parse_target(host_list):
    result_list = []
    for host in host_list:
        host = host.strip()
        re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')  # IP
        re_ips = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$')  # IPs
        re_url = re.compile('[^\s]*.[a-zA-Z]')  # URL
        re_ip_port = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')  # IP + Port
        re_url_port = re.compile('[^\s]*.[a-zA-Z]:\d{1,5}')  # URL + Port
        if re_ip.match(host):
            result_list.append(host)
        elif re_ips.match(host):
            hosts = ipaddr.IPv4Network(host).iterhosts()
            for ip in hosts:
                result_list.append(str(ip))
        elif re_url.match(host):
            result_list.append(host)
        elif re_ip_port.match(host):
            result_list.append(host)
        elif re_url_port.match(host):
            result_list.append(host)
        else:
            print("[!]", host, 'Target is not recognized as legal')
    return result_list

