#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-22
# @File    : vul_scanner.py
# @Desc    : ""

import time
from bson import ObjectId
from flask import Blueprint, render_template, request, jsonify
from mars.views.lib.parse_target import parse_target
from mars.views.lib.mongo_db import connectiondb, db_name_conf
from mars.views.authenticate import login_check
from mars.views.modules.vul_scanner.awvs_api import AcunetixScanner

vul_scanner = Blueprint('vul_scanner', __name__)
vul_db = db_name_conf()['vulscan_db']


@vul_scanner.route('/vul-scanner', methods=['GET', 'POST'])
@login_check
def vul_view():
    # scanner view
    if request.method == "GET":
        vul_task = connectiondb(vul_db).find()
        return render_template('vul-scanner.html', vul_task=vul_task)
    else:
        if request.form.get('source') == "new_scan":
            target_id = []
            task_name = request.form.get('task_name')
            target_list = request.form.get('target_addr').split("\n")
            scan_type = request.form.get('scan_type')
            description_val = request.form.get('description_val')
            for target in parse_target(target_list):
                target_id.append(AcunetixScanner().start_task(target, description_val, scan_type)['target_id'])
            task_data = {
                "task_name": task_name,
                "target_list": target_list,
                "scan_type": scan_type,
                "description": description_val,
                "status": "",
                "target_id": target_id,
                "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            }
            connectiondb(vul_db).insert(task_data)
            # print(new_scan)
            return "success"
        elif request.form.get('source') == "delete_task":
            task_id = request.form.get('delete')
            target_id = connectiondb(vul_db).find_one({"_id": ObjectId(task_id)})['target_id']
            if connectiondb(vul_db).remove({"_id": ObjectId(task_id)}):
                for t_id in target_id:
                    AcunetixScanner().delete_target(t_id)
                return "success"
            else:
                return "warning"
        elif request.form.get('source') == "download_report":
            task_id = request.form.get('task_id')
            target_id = connectiondb(vul_db).find_one({"_id": ObjectId(task_id)})['target_id']
            task_name = connectiondb(vul_db).find_one({"_id": ObjectId(task_id)})['task_name']
            report_url = AcunetixScanner().reports(target_id, 'targets', task_name)
            if report_url:
                return jsonify({"html_url": report_url[0], "pdf_url": report_url[1]})
            else:
                return "warning"


@vul_scanner.route('/vul-tasks', methods=['GET', 'POST'])
@login_check
def vul_tasks():
    # scanner view
    if request.method == "GET":
        try:
            tasks_info = AcunetixScanner().get_all()
        except Exception as e:
            print(e)
            tasks_info = ''
        return render_template('vul-tasks.html', tasks_info=tasks_info)
    else:
        if request.form.get('source') == "delete_scan":
            scan_id = request.form.get('delete')
            result = AcunetixScanner().delete_scan(scan_id)
            if result:
                return "success"
            else:
                return "warning"
        elif request.form.get('source') == "report":
            # scan_id type is list
            scan_id = [request.form.get('scan_id')]
            report_url = AcunetixScanner().reports(scan_id, 'scans', scan_id)
            if report_url:
                return jsonify({"html_url": report_url[0], "pdf_url": report_url[1]})
            else:
                return "warning"
