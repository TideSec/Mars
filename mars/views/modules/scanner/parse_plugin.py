#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-14
# @File    : parse_plugin.py
# @Desc    : ""


import os
import re
from mars.views.lib.mongo_db import connectiondb, db_name_conf
from flask import Flask

app = Flask(__name__)
plugin_db = db_name_conf()['plugin_db']


def parse_plugin(plugin_filename):
    name_pattern = re.compile(r'name\s*=\s*[\'\"\[](.*)[\'\"\]]')
    author_pattern = re.compile(r'author\s*=\s*[\'\"\[](.*)[\'\"\]]')
    date_pattern = re.compile(r'vulDate\s*=\s*[\'\"\[](.*)[\'\"\]]')
    app_pattern = re.compile(r'appName\s*=\s*[\'\"\[](.*)[\'\"\]]')
    type_pattern = re.compile(r'vulType\s*=\s*[\'\"\[](.*)[\'\"\]]')
    version_pattern = re.compile(r'appVersion\s*=\s*[\'\"\[](.*)[\'\"\]]')
    plugin_data = open(plugin_filename, 'r').read()
    try:
        plugin_name = name_pattern.findall(plugin_data)
        plugin_author = author_pattern.findall(plugin_data)
        plugin_date = date_pattern.findall(plugin_data)
        plugin_app = app_pattern.findall(plugin_data)
        plugin_type = type_pattern.findall(plugin_data)
        plugin_version = version_pattern.findall(plugin_data)
        plugin_info = {
            "plugin_filename": plugin_filename,
            "plugin_name": plugin_name[0],
            "plugin_author": plugin_author[0],
            "plugin_date": plugin_date[0],
            "plugin_app": plugin_app[0],
            "plugin_type": plugin_type[0],
            "plugin_version": plugin_version[0],
        }
        return plugin_info
    except Exception as e:
        print(e)
        pass


def local_install():
    print("[*]Processing...")
    connectiondb(plugin_db).drop()
    path = os.getcwd() + '/pocsuite_plugin/'
    files = os.listdir(path)
    for file_name in files:
        plugin_info = parse_plugin(path + file_name.strip())
        if plugin_info is None:
            pass
        else:
            db_insert = connectiondb(plugin_db).insert_one(plugin_info).inserted_id
    print("[*]Processing Completed!")


if __name__ == "__main__":
    local_install()
