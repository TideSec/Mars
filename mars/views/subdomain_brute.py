#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-18
# @File    : subdomain_brute.py
# @Desc    : ""

import time
import os
from threading import Thread
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response, send_from_directory
from bson import ObjectId
from lib.mongo_db import connectiondb, db_name_conf
from mars.views.authenticate import login_check
from mars.views.modules.subdomain import domain_brute

subdomain_brute = Blueprint('subdomain_brute', __name__)
domain_db = db_name_conf()['domain_db']
plugin_db = db_name_conf()['plugin_db']
subdomain_db = db_name_conf()['subdomain_db']


@subdomain_brute.route('/subdomain-brute', methods=['POST', 'GET'])
@login_check
def subdomain_view():
    if request.method == 'GET':
        # task delete
        if request.args.get('delete'):
            domain_id = request.args.get('delete')
            connectiondb(domain_db).delete_one({'_id': ObjectId(domain_id)})
            connectiondb(subdomain_db).remove({'domain_id': ObjectId(domain_id)})
            return redirect(url_for('subdomain_brute.subdomain_view'))

        # result download
        elif request.args.get('download'):
            domain_id = request.args.get('download')
            try:
                file_name = connectiondb(domain_db).find_one({'_id': ObjectId(domain_id)})['domain'][0]
                file_path = os.getcwd() + '/mars/static/download/'
                if os.path.exists(file_path + file_name):
                    os.remove(file_path + file_name)
                try:
                    for result in connectiondb(subdomain_db).find({'domain_id': ObjectId(domain_id)}):
                        with open(file_path + file_name, "a") as download_file:
                            download_file.write(result['subdomain'] + "\n")
                    sub_response = make_response(send_from_directory(file_path, file_name, as_attachment=True))
                    sub_response.headers["Content-Disposition"] = "attachment; filename=" + file_name
                    return sub_response
                except Exception as e:
                    return e
            except Exception as e:
                print(e)
        else:
            domain_data = connectiondb(domain_db).find().sort('date', -1)
            plugin_data = connectiondb(plugin_db).find()
            return render_template('subdomain-brute.html', domain_data=domain_data, plugin_data=plugin_data)

    # new domain
    elif request.method == 'POST':
        domain_name_val = request.form.get('domain_name_val')
        domain_val = request.form.get('domain_val').split('\n'),
        third_domain = request.form.get('third_domain')
        domain_list = list(domain_val)[0]
        if third_domain == "true":
            scan_option = 'Enable'
        else:
            scan_option = 'Disallow'
        domain_data = {
            'domain_name': domain_name_val,
            'domain': domain_list,
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'third_domain': scan_option,
            'status': "Preparation",
        }
        domain_id = connectiondb(domain_db).insert_one(domain_data).inserted_id
        if domain_id:
            # async domain brute
            t1 = Thread(target=domain_brute.start_domain_brute, args=(domain_list, domain_id))
            t1.start()
            return "success"


@subdomain_brute.route('/subdomain-list', methods=['POST', 'GET'])
@login_check
def subdomain_list():
    # Filter out the domain task
    if request.method == "GET":
        if request.args.get('domain'):
            domain_id = request.args.get('domain')
            sub_result = connectiondb(subdomain_db).find({'domain_id': ObjectId(domain_id)})
            return render_template('subdomain-list.html', sub_result=sub_result)

        # return subdomain for poc scan
        elif request.args.get('subdomain'):
            subdomain = []
            domain_id = request.args.get('subdomain')
            for i in connectiondb(subdomain_db).find({'domain_id': ObjectId(domain_id)}):
                subdomain.append(i['subdomain'])
            return '\n'.join(subdomain)

        # delete subdomain
        elif request.args.get('delete'):
            subdomain_id = request.args.get('delete')
            domain_id = connectiondb(subdomain_db).find_one({'_id': ObjectId(subdomain_id)})['domain_id']
            result = connectiondb(subdomain_db).delete_one({'_id': ObjectId(subdomain_id)})
            if result:
                return redirect(url_for('subdomain_brute.subdomain_list', domain=domain_id))

        # default view
        else:
            sub_result = connectiondb(subdomain_db).find()
            return render_template('subdomain-list.html', sub_result=sub_result)

