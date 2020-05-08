#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-14
# @File    : poc_scanner.py
# @Desc    : =_=!!

import sched
import time,hashlib
import datetime
from multiprocessing import Pool, Lock
from threading import RLock
from pocsuite.api.cannon import Cannon
from apscheduler.schedulers.blocking import BlockingScheduler
from bson.objectid import ObjectId
from mars.views.lib.mongo_db import connectiondb, db_name_conf
from mars.views.lib.parse_target import parse_target
from instance import config_name

config_db = db_name_conf()['config_db']
tasks_db = db_name_conf()['tasks_db']
vul_db = db_name_conf()['vul_db']
plugin_db = db_name_conf()['plugin_db']
server_db = db_name_conf()['server_db']


schedule = sched.scheduler(time.time, time.sleep)
lock = Lock()
thread_lock = RLock()

def md5hash(ip):
    md5 = hashlib.md5()
    md5.update(ip)
    return md5.hexdigest()

def insert_server_vul(vul_type,vul_name,vul_time,vul_result,hash):
    try:
        server_info = connectiondb(server_db).find_one({"hash": hash})
        print server_info
        if server_info:
            vulinfo = {"vul_type":vul_type,"vul_name":vul_name,"vul_time":vul_time,"vul_result":vul_result}
            vulinfo_tmp = []
            if server_info.has_key('vulinfo'):
                vulinfo_tmp = server_info['vulinfo']
                vulinfo_tmp.append(vulinfo)
            else:
                vulinfo_tmp.append(vulinfo)
            connectiondb(server_db).update({'hash':hash},{'$set':{"vulinfo":vulinfo_tmp}}, False, False)
    except Exception as e:
        print "Insert_server_info Error:",e

def verify_poc(scan_data):
    plugin_name = scan_data['plugin_name']
    plugin_filename = scan_data['plugin_filename']
    target = scan_data['target']
    info = {"pocname": plugin_name,
            "pocstring": open(plugin_filename, 'r').read(),
            "mode": 'verify'
            }
    try:
        invoker = Cannon(target, info)
        result = invoker.run()
        target_hash = md5hash(scan_data['target'])
        if result[-3][0] == 1:
            scan_result = {
                "plugin_filename": scan_data['plugin_filename'],
                "plugin_name": scan_data['plugin_name'],
                "plugin_id": scan_data['plugin_id'],
                "plugin_type": scan_data['plugin_type'],
                "plugin_app": scan_data['plugin_app'],
                "plugin_version": scan_data['plugin_version'],
                "target": scan_data['target'],
                "task_id": scan_data['task_id'],
                "task_name": scan_data['task_name'],
                "scan_result": result[-1],
                "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "hash":target_hash,
                "tag": ""
            }
            connectiondb(vul_db).insert(scan_result)
            #insert_server_vul("poc","plugin_filename",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),result[-1],hash)
    except Exception as e:
        raise e


class PocsuiteScanner:

    def __init__(self, task_id):
        self.task_id = task_id
        self.tasks_db_cursor = connectiondb(tasks_db).find_one({"_id": self.task_id})
        self.target_list = parse_target(self.tasks_db_cursor['scan_target'])
        self.plugin_id_list = self.tasks_db_cursor['plugin_id']
        self.result_tmp = []
        self.result = []
        self.processes = connectiondb(config_db).find_one({"config_name": config_name})['poc_thread']

    def set_scanner(self):
        connectiondb(tasks_db).update_one({'_id': ObjectId(self.task_id)}, {'$set': {'task_status': 'Processing'}})
        if connectiondb(vul_db).find_one({"task_id": self.task_id}):
            connectiondb(vul_db).update({'task_id': self.task_id}, {"$set": {"tag": "delete"}}, multi=True)
        pool_scanner = Pool(processes=self.processes)

        for target in self.target_list:
            for plugin_id in self.plugin_id_list:
                plugin_cursor = connectiondb(plugin_db).find_one({"_id": ObjectId(plugin_id)})
                scan_data = {
                    "plugin_filename": plugin_cursor['plugin_filename'].encode("UTF-8"),
                    "plugin_name": plugin_cursor['plugin_name'].encode("UTF-8"),
                    "plugin_id": plugin_cursor['_id'],
                    "plugin_type": plugin_cursor['plugin_type'],
                    "plugin_app": plugin_cursor['plugin_app'],
                    "plugin_version": plugin_cursor['plugin_version'],
                    "target": target,
                    "task_id": self.task_id,
                    "task_name": self.tasks_db_cursor['task_name'],
                }
                pool_scanner.apply_async(verify_poc, (scan_data,))
        pool_scanner.close()
        pool_scanner.join()

        connectiondb(tasks_db).update_one({'_id': ObjectId(self.task_id)}, {
            '$set': {
                'task_status': 'Completed',
                'end_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
        })


class PoCScannerLoop:
    def __init__(self):
        self.recursion = ''
        self.status = ''
        self.task_id = ''
        self.end_date = ''

    def task_schedule(self):
        scheduler = BlockingScheduler()
        try:
            scheduler.add_job(self._get_task, 'interval', seconds=30)
            scheduler.start()
        except Exception as e:
            print(e)

    def _get_task(self):
        # while thread_lock:
        for task_info in connectiondb(tasks_db).find():
            self.recursion = int(task_info['task_recursion'])
            self.task_id = task_info['_id']
            self.status = task_info['task_status']
            self.end_date = task_info['end_date']
            if self.recursion == 0:
                pass
            # every day task
            if self.recursion == 1:
                # print self.task_id
                # scanner = PocsuiteScanner(self.task_id)
                # scanner.set_scanner()
                # print "1111"
                if "Processing" in self.status:
                    pass
                else:
                    start_date = datetime.datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
                    plan_time = (datetime.datetime.now() - start_date).total_seconds()
                    if plan_time > 60 * 60 * 24:
                        print("Every day recursion start......")
                        scanner = PocsuiteScanner(self.task_id)
                        scanner.set_scanner()

            # every week task
            elif self.recursion == 7:
                if "Processing" in self.status:
                    pass
                else:
                    start_date = datetime.datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
                    plan_time = (datetime.datetime.now() - start_date).total_seconds()
                    if plan_time > 60 * 60 * 24 * 7:
                        print("Every week start...")
                        scanner = PocsuiteScanner(self.task_id)
                        scanner.set_scanner()
            # every month task
            elif self.recursion == 30:
                if "Processing" in self.status:
                    pass
                else:
                    start_date = datetime.datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
                    plan_time = (datetime.datetime.now() - start_date).total_seconds()
                    if plan_time > 60 * 60 * 24 * 30:
                        print("Every month start...")
                        scanner = PocsuiteScanner(self.task_id)
                        scanner.set_scanner()


if __name__ == '__main__':
    loop_scanner = PoCScannerLoop()

