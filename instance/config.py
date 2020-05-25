#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-10
# @File    : config.py
# @Desc    : ""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    def __init__(self):
        pass

    WEB_USER = 'admin'  # Web Auth User
    WEB_PASSWORD = 'tidesec'  # Web Auth Password
    POCSUITE_PATH = basedir + '/../Mars/views/modules/scanner/pocsuite_plugin/'
    AWVS_REPORT_PATH = basedir + '/../Mars/static/download/'  # static file download
    WEB_HOST = '0.0.0.0'  # Web Server Host
    WEB_PORT = 5000  # Web Server Port
    UPDATE_URL = "https://mars.tidesec.net/update"  # check update
    VERSION = '1.0.0'  # scanner version
    AWVS_URL = 'https://127.0.0.1:13443'  # Acunetix Web Vulnerability Scanner Url   tide@tidesec.com/Tide@2020
    AWVS_API_KEY = "1986ad8c0a5b3df4d7028d5f3c06e936c1f56bc11f1244d96b17edcd08940fbea"  # Acunetix Web Vulnerability Scanner API Key


class ProductionConfig(Config):
    DB_HOST = '127.0.0.1'  # MongoDB Host
    DB_PORT = 27017  # MongoDB Port (int)
    DB_NAME = 'mars'  # MongoDB Name
    DB_USERNAME = 'mars'  # MongoDB User
    DB_PASSWORD = 'tidesec.com'  # MongoDB Password
    CONFIG_NAME = 'mars'  # Scanner config name
    PLUGIN_DB = 'dev_plugin_info'  # Plugin collection
    TASKS_DB = 'dev_tasks'  # Scan tasks collection
    CUS_DB = 'dev_customer'  # Scan tasks collection
    VULNERABILITY_DB = 'dev_vuldb'  # Vulnerability collection
    ASSET_DB = 'dev_asset'  # Asset collection
    CONFIG_DB = 'dev_config'  # Scanner config collection
    SERVER_DB = 'dev_server'  # Asset server collection
    SUBDOMAIN_DB = 'dev_subdomain'  # Subdomain server collection
    DOMAIN_DB = 'dev_domain'  # Domain server collection
    PORT_DB = 'dev_port_scanner'  # Port scan collection
    AUTH_DB = 'dev_auth_tester'  # Auth tester tasks collection
    VULSCAN_DB = 'dev_vulscan'  # Acunetix scanner tasks collection
    WEEKPASSWD_DB = 'dev_week_passwd'  # Week password collection
    GITHUB_TASK_DB = 'dev_github_task'  # Github leaks tasks
    GITHUB_LEAK_DB = 'dev_github_leak'  # Github leaks info

