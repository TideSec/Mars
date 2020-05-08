#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-19
# @File    : domain_brute.py
# @Desc    : ""


import dns.resolver
from multiprocessing import Pool, Lock
from datetime import datetime
from random import sample
from string import digits, ascii_lowercase
from mars.views.lib.mongo_db import connectiondb, db_name_conf
from mars.views.lib.get_title import get_title
from instance import config_name

lock = Lock()
domain_db = db_name_conf()['domain_db']
config_db = db_name_conf()['config_db']
subdomain_db = db_name_conf()['subdomain_db']


def resolution(domain):
    _result = {}
    record_a = []
    record_cname = []
    try:
        respond = dns.resolver.query(domain.strip())
        for record in respond.response.answer:
            for i in record.items:
                if i.rdtype == dns.rdatatype.from_text('A'):
                    record_a.append(str(i))
                    _result[domain] = record_a
                elif i.rdtype == dns.rdatatype.from_text('CNAME'):
                    record_cname.append(str(i))
                    _result[domain] = record_cname
    except Exception as e:
        # print(e)
        pass
    return _result


class DomainBrute:

    def __init__(self, domain, domain_id):
        print("[*] %s %s Brute Start" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), domain))
        self.domain = domain
        self.domain_id = domain_id
        self.sub_domain = []
        self.third_domain = connectiondb(domain_db).find_one({"_id": domain_id})['third_domain']
        self.resolver_ip = ''
        self.result = ''
        self.thread = int(connectiondb(config_db).find_one({"config_name": config_name})['subdomain_thread'])
        self.subdomain_dict_2 = connectiondb(config_db).find_one({"config_name": config_name})['subdomain_dict_2']
        self.subdomain_dict_3 = connectiondb(config_db).find_one({"config_name": config_name})['subdomain_dict_3']
        self.random_subdomain = ''.join(sample(digits + ascii_lowercase, 10)) + '.' + domain

    def domain_handle(self):
        for sub_domain_2 in self.subdomain_dict_2:
            self.sub_domain.append(sub_domain_2.strip() + '.' + self.domain)
        if self.third_domain == "Enable":
            for sub_domain_3 in self.subdomain_dict_3:
                for sub_domain_2 in self.subdomain_dict_2:
                    sub_domain = sub_domain_3 + "." + sub_domain_2
                    self.sub_domain.append(sub_domain.strip() + '.' + self.domain)
        return self.sub_domain

    def resolver_check(self):
        try:
            var = resolution(self.random_subdomain)
            if var[self.random_subdomain]:
                return var[self.random_subdomain]
            else:
                return False
        except Exception as e:
            # print(e)
            return False

    def multi_brute(self):
        data_save = []
        result = []
        self.resolver_ip = self.resolver_check()
        pool = Pool(processes=self.thread)
        for sub_domain in self.domain_handle():
            result.append(pool.apply_async(resolution, (sub_domain,)))
        pool.close()
        pool.join()
        for res in result:
            self.result = res.get()
            for subdomain in self.result:
                if self.result[subdomain] != self.resolver_ip:
                    data = {
                        "subdomain": subdomain,
                        "domain": self.domain,
                        "domain_id": self.domain_id,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "result": self.result[subdomain],
                        "title": '',
                    }
                    data_save.append(data)
        try:
            if data_save:
                connectiondb(subdomain_db).insert_many(data_save, ordered=True)
        except Exception as e:
            print("[!] %s Saved result error: %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), e))
        print("[*] %s %s Brute Done" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.domain))


def start_domain_brute(domain_list, domain_id):
    time_start = datetime.now()
    print("[*] %s Domain Brute start %s" % (time_start.strftime("%Y-%m-%d %H:%M:%S"), domain_id))
    connectiondb(domain_db).update_one({"_id": domain_id}, {"$set": {
        "status": "Running"
    }})
    for domain in domain_list:
        start_brute = DomainBrute(domain, domain_id)
        start_brute.multi_brute()
    connectiondb(domain_db).update_one({"_id": domain_id}, {"$set": {
        "status": "Done"
    }})
    time_end = datetime.now()
    print("[*] %s Domain Brute Done %s" % (time_end.strftime("%Y-%m-%d %H:%M:%S"), domain_id))
    print("[*] %s Used Time: %s" % (time_end.strftime("%Y-%m-%d %H:%M:%S"), (time_end - time_start).seconds))
    get_domain_title(domain_id)


def get_domain_title(domain_id):
    pool = Pool(processes=50)
    result = []
    for i in connectiondb(subdomain_db).find({"domain_id": domain_id}):
        result.append(pool.apply_async(get_title, (i['subdomain'], i['_id'])))
    pool.close()
    pool.join()
    for res in result:
        lock.acquire()
        try:
            connectiondb(subdomain_db).update_one({"_id": res.get()["_id"]}, {"$set": {
                "title": res.get()['title']
            }})
        except Exception as e:
            print("update title error", e)
        lock.release()
