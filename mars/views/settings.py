#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-15
# @File    : settings.py
# @Desc    : ""

from flask import Blueprint, render_template, request
from lib.mongo_db import connectiondb, db_name_conf
from mars.views.authenticate import login_check
from instance import config_name

settings = Blueprint('settings', __name__)
config_db = db_name_conf()['config_db']


# system-config
@settings.route('/system-config', methods=['GET', 'POST'])
@login_check
def config_view():
    return render_template("system-config.html")


@settings.route('/advanced-option', methods=['GET', 'POST'])
@login_check
def option_view():
    if request.method == "GET":
        config_data = connectiondb(config_db).find_one({"config_name": config_name})
        config_info = {
            "poc_thread": config_data['poc_thread'],
            "discovery_thread": config_data['discovery_thread'],
            "subdomain_thread": config_data['subdomain_thread'],
            "port_thread": config_data['port_thread'],
            "auth_tester_thread": config_data['auth_tester_thread'],
            "subdomain_dict_2": '\n'.join(config_data['subdomain_dict_2']),
            "subdomain_dict_3": '\n'.join(config_data['subdomain_dict_3']),
            "username_dict": '\n'.join(config_data['username_dict']),
            "password_dict": '\n'.join(config_data['password_dict']),
            "discovery_time": config_data['discovery_time'],
            "port_list": ','.join('%s' % port for port in config_data['port_list']),
        }
        return render_template("advanced-option.html", config_info=config_info)
    else:
        # update thread config
        if request.form.get("source") == "thread_settings":
            update_config = {
                "poc_thread": int(request.form.get('poc_thread')),
                "discovery_thread": int(request.form.get('discovery_thread')),
                "subdomain_thread": int(request.form.get('subdomain_thread')),
                "port_thread": int(request.form.get('port_thread')),
                "auth_tester_thread": int(request.form.get('auth_tester_thread')),
                "discovery_time": request.form.get('discovery_time')
            }
            if connectiondb(config_db).update_one({'config_name': config_name}, {"$set": update_config}):
                return "success"
            else:
                return "Warning"
        # update subdomain_dict config
        elif request.form.get("source") == "subdomain_dict":
            update_config = {
                "subdomain_dict_2": request.form.get('subdomain_dict_2').split('\n'),
                "subdomain_dict_3": request.form.get('subdomain_dict_3').split('\n'),
            }
            if connectiondb(config_db).update_one({'config_name': config_name}, {"$set": update_config}):
                return "success"
            else:
                return "Warning"
        # update port_list config
        elif request.form.get("source") == "port_list":
            update_config = {
                "port_list": request.form.get('port_list').split(','),
            }
            if connectiondb(config_db).update_one({'config_name': config_name}, {"$set": update_config}):
                return "success"
            else:
                return "Warning"

        elif request.form.get("source") == "auth":
            update_config = {
                "username_dict": request.form.get('username_list').split('\n'),
                "password_dict": request.form.get('password_list').split('\n'),
            }

            if connectiondb(config_db).update_one({'config_name': config_name}, {"$set": update_config}):
                return "success"
            else:
                return "Warning"

        elif request.form.get("source") == "port_scan":
            update_config = {
                "port_list": request.form.get('port_list').split(','),
            }
            if connectiondb(config_db).update_one({'config_name': config_name}, {"$set": update_config}):
                return "success"
            else:
                return "Warning"
