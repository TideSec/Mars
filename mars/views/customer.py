#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-10
# @File    : customer.py
# @Desc    : ""

import time
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from bson import ObjectId
from threading import Thread
from lib.mongo_db import connectiondb, db_name_conf
from mars.views.modules.scanner.poc_scanner import PocsuiteScanner
from mars.views.authenticate import login_check


customer = Blueprint('customer', __name__)
tasks_db = db_name_conf()['tasks_db']
cus_db = db_name_conf()['cus_db']
asset_db = db_name_conf()['asset_db']
server_db = db_name_conf()['server_db']
subdomain_db = db_name_conf()['subdomain_db']
vul_db = db_name_conf()['vul_db']
plugin_db = db_name_conf()['plugin_db']


# tasks view
@customer.route('/cus-management')
@login_check
def cus_view():
    # delete task
    if request.args.get('delete'):
        task_id = request.args.get('delete')
        print "del task_id",task_id
        connectiondb(cus_db).delete_one({'_id': ObjectId(task_id)})
        connectiondb(asset_db).delete_many({'asset_cus_id': task_id})
        connectiondb(server_db).delete_many({'asset_cus_id': task_id})
        return "success"
    # rescan
    elif request.args.get('rescan'):
        task_id = request.args.get('rescan')
        connectiondb(asset_db).update_one({'asset_cus_id': ObjectId(task_id)}, {'$set': {'task_status': 'new'}})
        if connectiondb(server_db).find_one({"asset_cus_id": ObjectId(task_id)}):
            connectiondb(server_db).update({'asset_cus_id': ObjectId(task_id)}, {"$set": {"tag": "delete"}}, multi=True)


    # get task info for edit (get)
    elif request.args.get('edit'):
        cus_id = request.args.get('edit')
        cus_edit_data = connectiondb(cus_db).find_one({'_id': ObjectId(cus_id)})
        cus_edit_data_json = {
            "cus_name": cus_edit_data['cus_name'],
            "cus_contact": cus_edit_data['cus_contact'],
            "cus_phone": cus_edit_data['cus_phone'],
            "cus_email": cus_edit_data['cus_email'],
            "cus_zhouqi_start": cus_edit_data['cus_zhouqi_start'],
            "cus_zhouqi_end": cus_edit_data['cus_zhouqi_end'],
            "cus_serv_type": cus_edit_data['cus_serv_type'],
            "cus_other": cus_edit_data['cus_other'],

        }
        # print cus_edit_data_json
        return jsonify(cus_edit_data_json)

    # default task view
    cus_data = connectiondb(cus_db).find().sort('cus_add_time', 1)

    # cus_server_num = connectiondb(cus_db).find()

    cus_data_tmp = []

    for x in cus_data:
        cus_id = str(x['_id'])
        x['cus_server_num'] = connectiondb(server_db).find({'asset_cus_id': cus_id}).count()
        cus_data_tmp.append(x)

    return render_template('cus-management.html', cus_data=cus_data_tmp)


# task edit
@customer.route('/cus-edit', methods=['POST'])
@login_check
def cus_edit():
    # cus_name = request.form.get('cus_name')
    # task_plan = request.form.get('recursion_val')
    # target_text = request.form.get('target_val').split('\n', -1)
    cus_id = request.form.get('cus_id')
    cus_name =  request.form.get('cus_name')
    cus_contact =  request.form.get('cus_contact')
    cus_phone =  request.form.get('cus_phone')
    cus_email =  request.form.get('cus_email').strip()
    cus_zhouqi_start =  request.form.get('cus_zhouqi_start')
    cus_zhouqi_end =  request.form.get('cus_zhouqi_end')
    cus_serv_type =  request.form.get('cus_serv_type')
    cus_other =  request.form.get('cus_other')
    cus_add_time =  time.strftime('%Y-%m-%d %X',time.localtime(time.time()))

    update_task_data = connectiondb(cus_db).update_one(
        {'_id': ObjectId(cus_id)},
        {'$set': {
            'cus_name': cus_name,
            'cus_contact': cus_contact,
            'cus_phone': cus_phone,
            'cus_email':cus_email,
            'cus_zhouqi_start':cus_zhouqi_start,
            'cus_zhouqi_end':cus_zhouqi_end,
            'cus_serv_type':cus_serv_type,
            'cus_other':cus_other,
            'cus_add_time':cus_add_time,
        }
        }
    )
    if update_task_data:

        return 'success'


# new scan view
@customer.route('/new-customer', methods=['GET'])
@login_check
def customer_view():
    return render_template('new-customer.html')


# create task
@customer.route('/add-customer', methods=['POST'])
@login_check
def add_customer():
    # create task from new scan view (post)
    if request.form.get('source') == 'add_cus':
        cus_data = {

            "cus_name": request.form.get('cus_name'),
            "cus_contact": request.form.get('cus_contact'),
            "cus_phone": request.form.get('cus_phone'),
            "cus_email": request.form.get('cus_email').strip(),
            "cus_zhouqi_start": request.form.get('cus_zhouqi_start'),
            "cus_zhouqi_end": request.form.get('cus_zhouqi_end'),
            "cus_serv_type": request.form.get('cus_serv_type'),
            # "cus_serv_zhouqi": request.form.get('cus_serv_zhouqi'),
            "cus_other": request.form.get('cus_other'),
            "cus_add_time": time.strftime('%Y-%m-%d %X', time.localtime(time.time())),

        }

        if cus_data:
            existe_cus_datas = connectiondb(cus_db).find_one({'cus_name':cus_data['cus_name']})
            if not existe_cus_datas:
                cus_id = connectiondb(cus_db).insert_one(cus_data).inserted_id
                # print cus_data
                if cus_id:
                    # scanner = PocsuiteScanner(cus_id)
                    # t1 = Thread(target=scanner.set_scanner, args=())
                    # t1.start()
                    return "success"
            else:
                return 'repeat'
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


@customer.route('/vulnerability', methods=['POST', 'GET'])
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
