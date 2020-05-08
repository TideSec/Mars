#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-22
# @File    : awvs_api.py
# @Desc    : ""

import time
import os
import json
import requests
from flask import Flask
from instance import config

requests.packages.urllib3.disable_warnings()

ProductionConfig = config.ProductionConfig
app = Flask(__name__)
app.config.from_object(ProductionConfig)


class AcunetixScanner:

    def __init__(self):
        self.api_key = app.config.get('AWVS_API_KEY')
        self.scanner_url = app.config.get('AWVS_URL')
        self.awvs_report_path = app.config.get('AWVS_REPORT_PATH')
        self.scan_result = {}
        self.all_tasks = []
        self.report_url = []
        self.headers = {
            "X-Auth": self.api_key,
            "content-type": "application/json"
        }

    def new_scan(self, target, desc):
        data = {
            "address": target,
            "description": desc,
            "criticality": "10"
        }
        try:
            response = requests.post(self.scanner_url + "/api/v1/targets", data=json.dumps(data),
                                     headers=self.headers, timeout=30, verify=False)
            return json.loads(response.content)['target_id']
        except Exception as e:
            print(target, e)
            return False

    def start_task(self, target, desc, profile_id):
        profile_id_list = {'0': '11111111-1111-1111-1111-111111111111', '1': '11111111-1111-1111-1111-111111111112',
                           '2': '11111111-1111-1111-1111-111111111116', '3': '11111111-1111-1111-1111-111111111113',
                           '4': '11111111-1111-1111-1111-111111111115', '5': '11111111-1111-1111-1111-111111111117'}
        profile_id = profile_id_list[profile_id]
        target_id = self.new_scan(target, desc)
        data = {
            "target_id": target_id,
            "profile_id": profile_id,
            "schedule": {
                "disable": False,
                "start_date": None,
                "time_sensitive": False
            }
        }
        try:
            response = requests.post(self.scanner_url + "/api/v1/scans", data=json.dumps(data),
                                     headers=self.headers, timeout=30, verify=False)
            return json.loads(response.content)
        except Exception as e:
            print(target, target_id, e)
            return False

    def get_all(self):
        try:
            response = requests.get(self.scanner_url + "/api/v1/scans", headers=self.headers, timeout=30, verify=False)
            results = json.loads(response.content)
            task_info = {}
            for task in results['scans']:
                task_info['scan_id'] = task['scan_id']
                task_info['target_id'] = task['target_id']
                task_info['address'] = task['target']['address']
                task_info['desc'] = task['target']['description']
                task_info['profile_name'] = task['profile_name']
                task_info['status'] = task['current_session']['status']
                task_info['vul_high'] = task['current_session']['severity_counts']['high']
                task_info['vul_medium'] = task['current_session']['severity_counts']['medium']
                task_info['vul_low'] = task['current_session']['severity_counts']['low']
                task_info['vul_info'] = task['current_session']['severity_counts']['info']
                task_info['start_date'] = task['current_session']['start_date'][0:19].replace('T', ' ')
                self.all_tasks.append(task_info)
                task_info = {}
            return self.all_tasks
        except Exception as e:
            raise e

    def delete_scan(self, scan_id):
        try:
            response = requests.delete(self.scanner_url + "/api/v1/scans/" + str(scan_id),
                                       headers=self.headers, timeout=30, verify=False)
            if response.status_code == 204:
                return True
            else:
                return False
        except Exception as e:
                print(scan_id, e)
                return False

    def delete_target(self, target_id):
        try:
            response = requests.delete(self.scanner_url + "/api/v1/targets/" + str(target_id),
                                       headers=self.headers, timeout=30, verify=False)
            if response.status_code == 204:
                return True
            else:
                return False
        except Exception as e:
                print(target_id, e)
                return False

    def reports(self, id_list, list_type, task_name):
        # list_type = "scans", 'targets' ...
        data = {
            "template_id": "11111111-1111-1111-1111-111111111111",
            "source": {
                "list_type": list_type,
                "id_list": id_list
            }
        }
        try:
            response = requests.post(self.scanner_url + "/api/v1/reports", headers=self.headers,
                                     data=json.dumps(data), timeout=30, verify=False)
            if response.status_code == 201:
                while True:
                    res_down = requests.get(self.scanner_url + response.headers['Location'],
                                            headers=self.headers, timeout=30, verify=False)
                    if json.loads(res_down.content)['status'] == "completed":
                        for report_url in json.loads(res_down.content)['download']:
                            report_res = requests.get(self.scanner_url + report_url, timeout=30, verify=False)
                            report_name = time.strftime("%y%m%d", time.localtime()) + "_" + task_name[0] + '.' + report_url.split('.')[-1]
                            if os.path.exists(self.awvs_report_path + report_name):
                                os.remove(self.awvs_report_path + report_name)
                            with open(self.awvs_report_path + report_name, "wb") as report_content:
                                report_content.write(report_res.content)
                            self.report_url.append(report_name)
                        return self.report_url
            else:
                return False
        except Exception as e:
                print(id_list, e)
                return False
