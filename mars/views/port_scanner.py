#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-17
# @File    : port_scanner.py
# @Desc    : ""

import threading
import time
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from bson import ObjectId
from lib.mongo_db import connectiondb, db_name_conf
from mars.views.authenticate import login_check
from mars.views.modules.port_scanner.nmap_scanner import nmap_scanner
from instance import config_name

port_scanner = Blueprint('port_scanner', __name__)
config_db = db_name_conf()['config_db']
port_db = db_name_conf()['port_db']


# port_scanner
@port_scanner.route('/port-scanner', methods=['GET', 'POST'])
@login_check
def port_view():
    if request.method == "GET":
        if request.args.get("scan_id"):
            # default port scan result
            target_id = request.args.get("scan_id")
            db_course = connectiondb(port_db).find_one({"_id": ObjectId(target_id)})
            host = db_course['host']
            port = db_course['port']
            if db_course['status'] == "Done":
                result = '\n'.join('%s' % c for c in db_course['detail']).replace(';', " ")
            else:
                result = "Scanning, Please wait..."
            return render_template('port-scanner.html', host=host, result=result, port=port)
        elif request.args.get("result"):
            # table view port scan result
            scan_id = request.args.get("result")
            db_course = connectiondb(port_db).find_one({"_id": ObjectId(scan_id)})
            result = '\n'.join('%s' % c for c in db_course['detail'])
            return result
        elif request.args.get('delete'):
            # scan task delete
            scan_id = request.args.get("delete")
            connectiondb(port_db).delete_one({"_id": ObjectId(scan_id)})
            return redirect(url_for('port_scanner.port_view'))
        # default scan view
        port_list = connectiondb(config_db).find_one({"config_name": config_name})['port_list']
        ports = ','.join('%s' % port for port in port_list)
        return render_template('port-scanner.html', port_list=ports)
    else:
        # add scan
        if request.form.get('source') == "new_scan":
            target_val = request.form.get('target_val')
            arguments_val = int(request.form.get('arguments_val'))
            port_val = request.form.get('port_val')
            if len(port_val) > 0:
                if arguments_val == 0:
                    arguments = "-sT -T4 -p " + port_val
                elif arguments_val == 1:
                    arguments = "-sT -T4 --open -p " + port_val
                elif arguments_val == 2:
                    arguments = "-sS -T4 -Pn -p " + port_val
                elif arguments_val == 3:
                    arguments = "-sT -sV -O -A -p " + port_val
                else:
                    arguments = ""
            # use default port
            else:
                if arguments_val == 0:
                    arguments = "-sT -T4"
                elif arguments_val == 1:
                    arguments = "-sT -T4 --open"
                elif arguments_val == 2:
                    arguments = "-sS -T4 -Pn "
                elif arguments_val == 3:
                    arguments = "-sT -sV -O -A"
                else:
                    arguments = ""
            db_data = {
                "host": target_val,
                "status": "Preparation",
                'port': port_val,
                "arguments": arguments,
                'detail': "",
                'date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            scan_id = connectiondb(port_db).insert_one(db_data).inserted_id
            t1 = threading.Thread(target=nmap_scanner, args=(target_val, arguments, scan_id))
            t1.start()
            return jsonify({
                "result": "success",
                "scan_id": str(scan_id),
            })
