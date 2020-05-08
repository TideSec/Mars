#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-15
# @File    : dashboard.py
# @Desc    : ""

import datetime
import re
from collections import Counter
from flask import Blueprint, render_template
from bson import ObjectId
from lib.mongo_db import connectiondb, db_name_conf
from mars.views.authenticate import login_check

dashboard = Blueprint('dashboard', __name__)

vul_db = db_name_conf()['vul_db']
plugin_db = db_name_conf()['plugin_db']
tasks_db = db_name_conf()['tasks_db']
asset_db = db_name_conf()['asset_db']
weekpasswd_db = db_name_conf()['weekpasswd_db']
server_db = db_name_conf()['server_db']


@dashboard.route('/dashboard')
@login_check
def view_dashboard():
    dashboard_data = {
        "vul_count": get_count()['vul_count'],
        "plugin_count": get_count()['plugin_count'],
        "week_passwd_count": get_count()['week_passwd_count'],
        "server_count": get_count()['server_count'],
        "vul_trend_date": vul_trend()['date'],
        "vul_trend_count": vul_trend()['count'],
        "host_trend_count": host_trend()['count'],
        "host_trend_date": host_trend()['date'],
        "server_trend_count": server_trend()['count'],
        "server_trend_date": server_trend()['date'],
        "week_passwd_trend": week_passwd_trend()['count'],
        "vul_stats_name": vul_dist()[0],
        "vul_stats_count": vul_dist()[1],
        "password_stats_count": week_passwd_dist()[1],
        "password_stats_val": week_passwd_dist()[0],
    }
    return render_template('dashboard.html', dashboard_data=dashboard_data)


# get vul,plugin,week passwd,asset count
def get_count():
    asset_count = 0
    for i in connectiondb(asset_db).find():
        asset_count += len(i['asset_host'])
    count = {
        "vul_count": connectiondb(vul_db).count({"tag": {"$ne": "delete"}}),
        "week_passwd_count": connectiondb(weekpasswd_db).count({"tag": {"$ne": "delete"}}),
        "plugin_count": connectiondb(plugin_db).count(),
        "server_count": connectiondb(server_db).count()
    }
    return count


# Vulnerability Trend dashboard
def vul_trend():
    vul_day_count = []
    vul_date_list = []
    vul_trend_info = {}
    now_date = datetime.datetime.now()
    for scan_date in range(6, -1, -1):
        vul_date = (now_date - datetime.timedelta(scan_date)).strftime("%Y-%m-%d")
        vul__day_count = connectiondb(vul_db).find({'date': re.compile(vul_date)}).count()
        vul_day_count.append(vul__day_count)
        vul_date_list.append(vul_date)
        vul_trend_info['date'] = vul_date_list
        vul_trend_info['count'] = vul_day_count
    return vul_trend_info


# host
def host_trend():
    host_day_count = []
    host_date_list = []
    host_trend_info = {}
    now_date = datetime.datetime.now()
    for scan_date in range(6, -1, -1):
        host_date = (now_date - datetime.timedelta(scan_date)).strftime("%Y-%m-%d")
        host__day_count = connectiondb(server_db).find({"updatetime": re.compile(host_date),"task_type":'host'}).count()
        host_day_count.append(host__day_count)
        host_date_list.append(host_date)
        host_trend_info['date'] = host_date_list
        host_trend_info['count'] = host_day_count
    return host_trend_info


# server
def server_trend():
    server_day_count = []
    server_date_list = []
    server_trend_info = {}
    now_date = datetime.datetime.now()
    for scan_date in range(6, -1, -1):
        server_date = (now_date - datetime.timedelta(scan_date)).strftime("%Y-%m-%d")
        server__day_count = connectiondb(server_db).find({"updatetime": re.compile(server_date),"task_type":"web"}).count()
        server_day_count.append(server__day_count)
        server_date_list.append(server_date)
        server_trend_info['date'] = server_date_list
        server_trend_info['count'] = server_day_count
    return server_trend_info


def week_passwd_trend():
    week_passwd_info = {}
    week_passwd_count = []
    now_date = datetime.datetime.now()
    for scan_date in range(6, -1, -1):
        _date = (now_date - datetime.timedelta(scan_date)).strftime("%Y-%m-%d")
        count = connectiondb(weekpasswd_db).find({'date': re.compile(_date)}).count()
        week_passwd_count.append(count)
        week_passwd_info['count'] = week_passwd_count
    return week_passwd_info


# Vulnerability Distribution
def vul_dist():
    plugin_count_list = []
    plugin_stats_name = []
    plugin_stats_count = []
    for i in connectiondb(vul_db).find():
        plugin_count_list.append(i['plugin_name'])
    word_counts = Counter(plugin_count_list)
    top_10 = word_counts.most_common(10)
    for i in top_10:
        plugin_name = i[0]
        vul_count = i[1]
        plugin_stats_name.append(plugin_name)
        plugin_stats_count.append(vul_count)
    return plugin_stats_name, plugin_stats_count


# Week password Distribution
def week_passwd_dist():
    tmp_list = []
    week_passwd_name = []
    week_passwd_count = []
    for i in connectiondb(weekpasswd_db).find():
        tmp_list.append(i['password'])
    word_counts = Counter(tmp_list)
    top_10 = word_counts.most_common(10)
    for i in top_10:
        week_passwd_name.append(i[0])
        week_passwd_count.append(i[1])
    return week_passwd_name, week_passwd_count


def asset_server():
    pass
