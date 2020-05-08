#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-17
# @File    : nmap_scanner.py
# @Desc    : ""

import nmap
from mars.views.lib.mongo_db import connectiondb, db_name_conf

port_db = db_name_conf()['port_db']


class NmapScanner:
    def __init__(self, target, arguments, scan_id):
        self.target = target
        self.arguments = arguments
        self.scan_id = scan_id
        self.ports = []
        self.result = []

    def scan(self):
        port_scanner = nmap.PortScanner()
        try:
            port_scanner.scan(self.target, arguments=self.arguments)
        except Exception as e:
            print self.target, e
        return port_scanner

    def port_result(self):
        self.result.append(self.scan().command_line())
        for i in self.scan().csv().split('\r\n'):
            self.result.append(i)
        self.result.pop(1)
        connectiondb(port_db).update_one({"_id": self.scan_id}, {'$set': {
            'status': 'Done',
            'detail': self.result
        }})
        return self.result


def nmap_scanner(target_val, option_val, scan_id):
    new_scan = NmapScanner(target_val, option_val, scan_id)
    new_scan.port_result()


if __name__ == '__main__':
    nmap_scanner('127.0.0.1', '-p', '80')
