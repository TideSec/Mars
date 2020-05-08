#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-30
# @File    : asset_discovery.py
# @Desc    : ""

import nmap
import time
from multiprocessing import Pool
from apscheduler.schedulers.blocking import BlockingScheduler
from mars.views.lib.mongo_db import connectiondb, db_name_conf
from mars.views.lib.parse_target import parse_target
from instance import config_name

config_db = db_name_conf()['config_db']
asset_db = db_name_conf()['asset_db']
server_db = db_name_conf()['server_db']


class AssetDiscovery:
    def __init__(self, asset_id):
        self.asset_id = asset_id
        self.result_tmp = []
        self.result = []
        self.port_list = connectiondb(config_db).find_one({"config_name": config_name})['port_list']
        self.processes = connectiondb(config_db).find_one({"config_name": config_name})['discovery_thread']
        self.asset_name = connectiondb(asset_db).find_one({"_id": self.asset_id})['asset_name']
        self.host_list = parse_target(connectiondb(asset_db).find_one({"_id": self.asset_id})['asset_host'])

    def set_discovery(self):
        print("[*] %s Discovery start..." % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        pool_port = Pool(processes=self.processes)
        for host in self.host_list:
            self.result_tmp.append(pool_port.apply_async(port_scanner, (host, self.port_list)))
        pool_port.close()
        pool_port.join()
        for res_tmp in self.result_tmp:
            try:
                if res_tmp.get():
                    for i in res_tmp.get():
                        self.result.append(i)
            except Exception as e:
                print(e)
                pass
        print("[*] %s Discovery done..." % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("[*] %s Saving discovery result..." % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.save_result()
        print("[*] %s Save discovery done..." % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def save_result(self):
        if connectiondb(server_db).find_one({"asset_id": self.asset_id}):
            connectiondb(server_db).update({"asset_id": self.asset_id}, {"$set": {"tag": "delete"}}, multi=True)
        for res in self.result:
            res['asset_name'] = self.asset_name
            res['asset_id'] = self.asset_id
            res['tag'] = ""
            res['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            try:
                connectiondb(server_db).insert_one(res)
            except Exception as e:
                print("[!] Save discovery result error %s" % e)


def port_scanner(host, port_list):
    result = []
    scanner = nmap.PortScanner()
    arguments = "-sT -sV -sC -A -Pn -p " + ','.join('%s' % port for port in port_list)
    try:
        # port processing
        scanner.scan(host, arguments=arguments)
        # port 'state' == 'open'
        # print("Scanning: %s" % host)
        for port in scanner[host].all_tcp():
            if scanner[host]['tcp'][port]['state'] == 'open':
                if "script" in scanner[host]['tcp'][port].keys():
                    script = scanner[host]['tcp'][port]['script']
                else:
                    script = ''
                if len(scanner[host]['tcp'][port]['version']) > 0:
                    version = scanner[host]['tcp'][port]['version']
                else:
                    version = 'Unknown'
                if len(scanner[host]['tcp'][port]['product']) > 0:
                    product = scanner[host]['tcp'][port]['product']
                else:
                    product = scanner[host]['tcp'][port]['name']
                data = {
                    "product": product,
                    "version": version,
                    "name": scanner[host]['tcp'][port]['name'],
                    "script": script,
                    "extrainfo": scanner[host]['tcp'][port]['extrainfo'],
                    "cpe": scanner[host]['tcp'][port]['cpe'],
                    "host": host,
                    "port": port,
                }
                result.append(data)
        return result
    except Exception as msg:
        print(msg)
        pass
    return result


class DiscoveryLoop:

    def __init__(self):
        self.sche_time = connectiondb(config_db).find_one({"config_name": config_name})['discovery_time'].split(":")
        self.asset_id = ''
        self.discover_option = ''

    def task_schedule(self):
        scheduler = BlockingScheduler()
        try:
            scheduler.add_job(self._get_task, 'cron', day='1-31', hour=self.sche_time[0],
                              minute=self.sche_time[1], second=self.sche_time[2])
            scheduler.start()
        except Exception as e:
            print(e)

    def _get_task(self):
        print("Discovery scheduler success")
        for asset_info in connectiondb(asset_db).find():
            self.discover_option = asset_info['discover_option']
            if self.discover_option == "Enable":
                self.asset_id = asset_info['_id']
                try:
                    AssetDiscovery(self.asset_id).set_discovery()
                except Exception as e:
                    print(e)
                    return e
        print("Discovery scheduler done")


