#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-10
# @File    : poc_scanner.py
# @Desc    : ""

import time
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from bson import ObjectId
from threading import Thread
from lib.mongo_db import connectiondb, db_name_conf
from mars.views.modules.scanner.poc_scanner import PocsuiteScanner
from mars.views.authenticate import login_check


poc_scanner = Blueprint('poc_scanner', __name__)
tasks_db = db_name_conf()['tasks_db']
asset_db = db_name_conf()['asset_db']
server_db = db_name_conf()['server_db']
subdomain_db = db_name_conf()['subdomain_db']
vul_db = db_name_conf()['vul_db']
plugin_db = db_name_conf()['plugin_db']


# tasks view
@poc_scanner.route('/task-management')
@login_check
def tasks_view():
    # delete task
    if request.args.get('delete'):
        task_id = request.args.get('delete')
        connectiondb(tasks_db).delete_one({'_id': ObjectId(task_id)})
        connectiondb(vul_db).update({'task_id': ObjectId(task_id)}, {"$set": {"tag": "delete"}}, multi=True)
        return "success"
    # rescan
    elif request.args.get('rescan'):
        task_id = request.args.get('rescan')
        connectiondb(tasks_db).update_one({'_id': ObjectId(task_id)}, {'$set': {'task_status': 'Preparation'}})
        if connectiondb(vul_db).find_one({"task_id": ObjectId(task_id)}):
            connectiondb(vul_db).update({'task_id': ObjectId(task_id)}, {"$set": {"tag": "delete"}}, multi=True)
        try:
            scanner = PocsuiteScanner(ObjectId(task_id))
            t1 = Thread(target=scanner.set_scanner, args=())
            t1.start()
            return "success"
        except Exception as e:
            raise e

    # get task info for edit (get)
    elif request.args.get('edit'):
        task_id = request.args.get('edit')
        task_edit_data = connectiondb(tasks_db).find_one({'_id': ObjectId(task_id)})
        task_edit_data_json = {
            'task_name': task_edit_data['task_name'],
            'scan_target': '\n'.join(task_edit_data['scan_target']),
        }
        return jsonify(task_edit_data_json)

    # default task view
    task_data = connectiondb(tasks_db).find().sort('end_date', -1)
    return render_template('task-management.html', task_data=task_data)


# task edit
@poc_scanner.route('/task-edit', methods=['POST'])
@login_check
def tasks_edit():
    # task update
    task_name = request.form.get('taskname_val')
    task_plan = request.form.get('recursion_val')
    target_text = request.form.get('target_val').split('\n', -1)
    task_id = request.form.get('task_id')
    update_task_data = connectiondb(tasks_db).update_one(
        {'_id': ObjectId(task_id)},
        {'$set': {
            'task_name': task_name,
            'task_recursion': task_plan,
            'scan_target': target_text,
        }
        }
    )
    if update_task_data:
        scanner = PocsuiteScanner(ObjectId(task_id))
        t1 = Thread(target=scanner.set_scanner, args=())
        t1.start()
        return 'success'


# new scan view
@poc_scanner.route('/new-scan', methods=['GET'])
@login_check
def scan_view():
    # default create scan view

    plugin_info = connectiondb(plugin_db).find()
    asset_info = connectiondb(asset_db).find().sort('asset_name',1)
    asset_info_tmp = []

    for x in asset_info:
        asset_task_id = str(x['_id'])
        x['asset_server_num'] = connectiondb(server_db).find({'asset_task_id': asset_task_id}).count()
        asset_info_tmp.append(x)

    return render_template('new-scan.html', asset_info=asset_info_tmp,plugin_info=plugin_info)


# create task
@poc_scanner.route('/add-task', methods=['POST'])
@login_check
def add_task():
    # create task from new scan view (post)
    if request.form.get('source') == 'scan_view':
        server_target_tmp = []

        asset_id_val = request.form.get('asset_id_val').split(',', -1)
        for id_tmp in asset_id_val:
            server_info_tmp = connectiondb(server_db).find({'asset_task_id': id_tmp},{ "_id": 0, "target": 1 })
            for tmp_1 in server_info_tmp:
                if tmp_1.has_key('target'):
                    server_target_tmp.append(tmp_1['target'])
            # asset_target_val  = ','.join(server_target_tmp)

        scan_target_tmp = request.form.get('target_val').replace('\r', '').split('\n', -1)
        for tmp_2 in scan_target_tmp:
            if tmp_2:
                server_target_tmp.append(tmp_2)

        task_data = {
            "task_name": time.strftime("%y%m%d", time.localtime()) + "_" + request.form.get('taskname_val'),
            "task_recursion": request.form.get('recursion_val'),
            "scan_target":server_target_tmp,
            "plugin_id": request.form.get('plugin_val').split(',', -1),
            "start_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "end_date": "-",
            "task_status": "new"
        }

        # print task_data
        if task_data:
            task_id = connectiondb(tasks_db).insert_one(task_data).inserted_id
            if task_id:
                scanner = PocsuiteScanner(task_id)
                t1 = Thread(target=scanner.set_scanner, args=())
                t1.start()
                return "success"
        else:
            return 'error'

    # create task from asset (post)
    elif request.form.get('source') == 'asset':
        task_data = {
            "task_name": time.strftime("%y%m%d", time.localtime()) + "_" + request.form.get('taskname_val'),
            "task_recursion": request.form.get('recursion_val'),
            "scan_target": request.form.get('target_val').replace('\r', '').split('\n', -1),
            "plugin_id": request.form.get('plugin_val').split(',', -1),
            "start_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "end_date": "-",
            "task_status": "Preparation"
        }
        if task_data:
            task_id = connectiondb(tasks_db).insert_one(task_data).inserted_id
            if task_id:
                scanner = PocsuiteScanner(task_id)
                t1 = Thread(target=scanner.set_scanner, args=())
                t1.start()
                return 'success'
        else:
            return 'error'
    # create task from sub domain (post)
    elif request.form.get('source') == 'subdomain':
        task_data = {
            "task_name": time.strftime("%y%m%d", time.localtime()) + "_" + request.form.get('taskname_val'),
            "task_recursion": request.form.get('recursion_val'),
            "scan_target": request.form.get('target_val').replace('\r', '').split('\n', -1),
            "plugin_id": request.form.get('plugin_val').split(',', -1),
            "start_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "end_date": "-",
            "task_status": "Preparation"
        }
        if task_data:
            task_id = connectiondb(tasks_db).insert_one(task_data).inserted_id
            if task_id:
                scanner = PocsuiteScanner(task_id)
                t1 = Thread(target=scanner.set_scanner, args=())
                t1.start()
                return 'success'
        else:
            return 'error'


@poc_scanner.route('/vulnerability', methods=['POST', 'GET'])
@login_check
def vulnerability_view():
    if request.method == "GET":
        # vulnerability delete
        if request.args.get('delete'):
            vul_id = request.args.get('delete')
            # task_id = connectiondb(vul_db).find_one({'_id': ObjectId(vul_id)})['task_id']
            # connectiondb(vul_db).delete_one({'_id': ObjectId(vul_id)})
            connectiondb(vul_db).update({'_id': ObjectId(vul_id)}, {"$set": {"tag": "delete"}}, multi=True)
            return redirect(url_for('poc_scanner.vulnerability_view'))

        # vulnerability rescan (Not completed)
        elif request.args.get('rescan'):
            vul_id = request.args.get('rescan')
            print(vul_id)
            # Not completed

        # vulnerability details
        elif request.args.get('result'):
            vul_id = request.args.get('result')
            vul_info = connectiondb(vul_db).find_one({'_id': ObjectId(vul_id)})
            del vul_info['_id']
            del vul_info['task_id']
            del vul_info['plugin_id']
            if vul_info:
                return jsonify(vul_info)
            else:
                return jsonify({"result": "Get details error"})

        # from task view  screening vulnerabilities by task_id
        elif request.args.get('task'):
            task_id = request.args.get('task')
            vul_data = connectiondb(vul_db).find({'task_id': ObjectId(task_id), "tag": {"$ne": "delete"}}).sort(
                'scan_date', -1)

            return render_template('vulnerability.html', vul_data=vul_data)

        # from plugin view  screening vulnerabilities by plugin_id
        elif request.args.get('plugin'):
            plugin_id = request.args.get('plugin')
            vul_data = connectiondb(vul_db).find({'plugin_id': ObjectId(plugin_id),
                                                  "tag": {"$ne": "delete"}}).sort('date', -1)
            return render_template('vulnerability.html', vul_data=vul_data)

        # default vulnerability view
        vul_data = connectiondb(vul_db).find({"tag": {"$ne": "delete"}}).sort('date', -1)
        return render_template('vulnerability.html', vul_data=vul_data)

    elif request.method == "POST":
        # delete multiple choices
        # Not completed
        return jsonify({'result': 'success'})
