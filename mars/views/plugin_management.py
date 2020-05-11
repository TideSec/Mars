#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-14
# @File    : plugin_management.py
# @Desc    : ""

import time
import os
from flask import Flask, Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from bson import ObjectId
from lib.mongo_db import connectiondb, db_name_conf
from mars.views.authenticate import login_check
from mars.views.modules.scanner.parse_plugin import parse_plugin
from instance import config


ProductionConfig = config.ProductionConfig
app = Flask(__name__)
app.config.from_object(ProductionConfig)

plugin_management = Blueprint('plugin_management', __name__)
tasks_db = db_name_conf()['tasks_db']
asset_db = db_name_conf()['asset_db']
server_db = db_name_conf()['server_db']
subdomain_db = db_name_conf()['subdomain_db']
vul_db = db_name_conf()['vul_db']
plugin_db = db_name_conf()['plugin_db']


# new plugin
# @plugin_management.route('/new-asset', methods=['GET', 'POST'])
# @login_check
# def new_plugin():
#     pass


@plugin_management.route('/plugin-management', methods=['GET', 'POST'])
@login_check
def plugin_view():
    # delete plugin
    if request.method == "GET":
        if request.args.get("delete"):
            plugin_id = request.args.get('delete')
            plugin_filename = connectiondb(plugin_db).find_one({"_id": ObjectId(plugin_id)})['plugin_filename']
            if connectiondb(plugin_db).delete_one({'_id': ObjectId(plugin_id)}):
                try:
                    os.remove(plugin_filename)
                except Exception as e:
                    raise e
                return "success"
            else:
                return "Warning"
        # get plugin info
        elif request.args.get("info"):
            plugin_id = request.args.get('info')
            plugin_info_data = connectiondb(plugin_db).find_one({'_id': ObjectId(plugin_id)})
            del plugin_info_data['_id']
            if plugin_info_data:
                return jsonify(plugin_info_data)
            else:
                return jsonify({"result": "Warning"})
        else:
            # default view
            plugin_info = connectiondb(plugin_db).find()
            return render_template("plugin-management.html", plugin_info=plugin_info)
    else:
        # delete select plugin
        if request.form.get('source') == 'delete_select':
            plugins_list = request.form.get('plugins_list').split(',')
            for plugin_id in plugins_list:
                plugin_filename = connectiondb(plugin_db).find_one({"_id": ObjectId(plugin_id)})['plugin_filename']
                if connectiondb(plugin_db).delete_one({'_id': ObjectId(plugin_id)}):
                    try:
                        os.remove(plugin_filename)
                    except Exception as e:
                        print(e)
                        return 'success'
            return 'success'


@plugin_management.route('/plugin-upload', methods=['GET', 'POST'])
@login_check
def plugin_upload():
    file_path = app.config.get('POCSUITE_PATH')
    file_data = request.files['file']
    if file_data:
        file_name = "_" + time.strftime("%y%m%d", time.localtime()) + "_" + secure_filename(file_data.filename)
        save_path = file_path + file_name
        file_data.save(save_path)
        try:
            new_plugin_info = parse_plugin(save_path)
            if new_plugin_info:
                db_insert = connectiondb(plugin_db).insert_one(new_plugin_info).inserted_id
                if db_insert:
                    return jsonify({"result": "success"})
            else:
                return jsonify({"result": "Warning"})
        except Exception as e:
            print(e)
            return "Warning"
