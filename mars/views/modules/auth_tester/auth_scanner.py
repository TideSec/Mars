#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-6-19
# @File    : auth_scanner.py
# @Desc    : ""

import time
from threading import Thread
from datetime import datetime
from multiprocessing import Pool
from mars.views.lib.mongo_db import connectiondb, db_name_conf
from mars.views.modules.auth_tester.hydra_plugin import HydraScanner, ServiceCheck
from mars.views.lib.parse_target import parse_target
from apscheduler.schedulers.blocking import BlockingScheduler
from instance import config_name

config_db = db_name_conf()['config_db']
weekpasswd_db = db_name_conf()['weekpasswd_db']
auth_db = db_name_conf()['auth_db']


def hydra_scanner(target_list, service, username_list, password_list, args):
    start = HydraScanner(target_list, service, username_list, password_list, args)
    result = start.scanner()
    return result


def service_check(target_list, service, args):
    start = ServiceCheck(target_list, service, args)
    result = start.service_check()
    return result


class AuthCrack:

    def __init__(self, task_id):
        self.task_id = task_id
        self.db_cursor = connectiondb(auth_db).find_one({"_id": self.task_id})
        self.processes = connectiondb(config_db).find_one({"config_name": config_name})['auth_tester_thread']
        self.task_name = self.db_cursor['task_name']
        self.username_list = self.db_cursor['username']
        self.password_list = self.db_cursor['password']
        self.target_list = parse_target(self.db_cursor['target'])
        self.check_result = {}
        self.online_target = []
        self.service_list = self.db_cursor['service']
        self.args = self.db_cursor['args']
        self.result_pool = []
        self.result = []
        self.week_count = 0

    def start_scan(self):
        connectiondb(auth_db).update_one({"_id": self.task_id}, {"$set": {"status": "Processing"}})
        # start host check
        tmp_result = []
        check_time = datetime.now()
        print("[*] %s %s Service Check..." % (check_time.strftime("%Y-%m-%d %H:%M:%S"), self.task_name))
        for service in self.service_list:
            # Filter online host
            pool_a = Pool(processes=self.processes)
            for target in self.target_list:
                tmp_result.append(pool_a.apply_async(service_check, (target, service, self.args)))
            pool_a.close()
            pool_a.join()
            for res_a in tmp_result:
                if res_a.get():
                    target = res_a.get()['target']
                    check_res = res_a.get()['result']
                    if check_res:
                        username = check_res['username']
                        password = check_res['password']
                        if not username:
                            username = "None"
                        if not password:
                            password = "None"
                        self.save_result(target, service, username, password)
                    else:
                        self.online_target.append(target)
            self.check_result[service] = self.online_target
            self.online_target = []
            tmp_result = []
        check_end_time = datetime.now()
        print("[*] %s %s Service Check Done..." % (check_end_time.strftime("%Y-%m-%d %H:%M:%S"), self.task_name))
        print("[*] %s Service check used time: %ss" % (self.task_name, (check_end_time - check_time).seconds))
        # start crack
        print("[*] %s %s Crack Start..." % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.task_name))
        pool_b = Pool(processes=self.processes)
        for service, target_list in self.check_result.items():
            # print(service, target_list)
            self.result.append(pool_b.apply_async(hydra_scanner, (target_list, service, self.username_list,
                                                                  self.password_list, self.args)))
        pool_b.close()
        pool_b.join()
        print("[*] %s %s Crack Done..." % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.task_name))
        for res_b in self.result:
            if res_b.get():
                for i in res_b.get():
                    target = i['target']
                    service = i['service']
                    username = i['username']
                    password = i['password']
                    self.save_result(target, service, username, password)
        print("[*] %s Crack used time: %ss" % (self.task_name, (datetime.now() - check_time).seconds))
        print("[*] %s %s Saving result..." % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.task_name))
        connectiondb(auth_db).update_one({"_id": self.task_id}, {"$set": {
            "status": "Completed",
            "week_count": self.week_count,
        }})
        print("[*] %s %s Save result done..." % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.task_name))

    def save_result(self, target, service, username, password):
        data = {
            "target": target,
            "service": service,
            "username": username,
            "password": password,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task_id": self.task_id,
            "task_name": self.task_name,
            "tag": ""
        }
        self.week_count += 1
        connectiondb(weekpasswd_db).insert_one(data)


class AuthTesterLoop:

    def __init__(self):
        self.recursion = ''
        self.status = ''
        self.scan_date = ''
        self.task_id = ''

    def task_schedule(self):
        scheduler = BlockingScheduler()
        try:
            scheduler.add_job(self._get_task, 'interval', seconds=30)
            scheduler.start()
        except Exception as e:
            print(e)

    def _get_task(self):
        for task_info in connectiondb(auth_db).find():
            self.recursion = task_info['recursion']
            self.status = task_info['status']
            self.scan_date = task_info['date']
            self.task_id = task_info['_id']
            start_date = datetime.strptime(self.scan_date, "%Y-%m-%d %H:%M:%S")
            plan_time = (datetime.now() - start_date).total_seconds()
            if self.recursion == 0:
                pass
            # every day
            elif self.recursion == 1 and "Completed" in self.status:
                if plan_time > 60 * 60 * 24 * 1:
                    if self.start_loop_scan():
                        print("[*] Every Day Task Start...", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # every week
            elif self.recursion == 7 and "Completed" in self.status:
                if plan_time > 60 * 60 * 24 * 7:
                    if self.start_loop_scan():
                        print("[*] Every Week Task Start...", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # every month
            elif self.recursion == 30 and "Completed" in self.status:
                if plan_time > 60 * 60 * 24 * 30:
                    if self.start_loop_scan():
                        print("[*] Every Month Task Start...", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def start_loop_scan(self):
        connectiondb(weekpasswd_db).update({"task_id": self.task_id}, {"$set": {"tag": "delete"}}, multi=True)
        connectiondb(auth_db).update_one({"_id": self.task_id}, {"$set": {
            "status": "Queued",
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "week_count": 0,
        }})
        scanner = AuthCrack(self.task_id)
        if scanner:
            t1 = Thread(target=scanner.start_scan, args=())
            t1.start()
            return True
