#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-10
# @File    : mongo_db.py
# @Desc    : ""

from flask import Flask
from pymongo import MongoClient
from instance import config

ProductionConfig = config.ProductionConfig
app = Flask(__name__)
app.config.from_object(ProductionConfig)
db_host = app.config.get('DB_HOST')
db_port = app.config.get('DB_PORT')
db_username = app.config.get('DB_USERNAME')
db_password = app.config.get('DB_PASSWORD')
db_name = app.config.get('DB_NAME')


def connectiondb(collection):
    client = MongoClient(db_host, db_port)
    db = client[db_name]
    db.authenticate(db_username, db_password)
    dbcollection = db[collection]
    return dbcollection


def db_management(command):
    client = MongoClient(db_host, db_port)
    db = client[db_name]
    db.authenticate(db_username, db_password)
    if command == 'collection_names':
        result = db.collection_names()
        return result


def db_name_conf():
    asset_db = app.config.get('ASSET_DB')
    tasks_db = app.config.get('TASKS_DB')
    cus_db = app.config.get('CUS_DB')
    vul_db = app.config.get('VULNERABILITY_DB')
    plugin_db = app.config.get('PLUGIN_DB')
    config_db = app.config.get('CONFIG_DB')
    server_db = app.config.get('SERVER_DB')
    subdomain_db = app.config.get('SUBDOMAIN_DB')
    domain_db = app.config.get('DOMAIN_DB')
    weekpasswd_db = app.config.get('WEEKPASSWD_DB')
    port_db = app.config.get('PORT_DB')
    auth_db = app.config.get('AUTH_DB')
    # search_db = app.config.get('SEARCH_DB')
    vulscan_db = app.config.get('VULSCAN_DB')
    db_name_dict = {
        'asset_db': asset_db,
        'tasks_db': tasks_db,
        'cus_db':cus_db,
        'vul_db': vul_db,
        'plugin_db': plugin_db,
        'config_db': config_db,
        'server_db': server_db,
        'subdomain_db': subdomain_db,
        'domain_db': domain_db,
        'weekpasswd_db': weekpasswd_db,
        'port_db': port_db,
        'auth_db': auth_db,
        # 'search_db': search_db,
        'vulscan_db': vulscan_db,
    }
    return db_name_dict


if __name__ == "__main__":
    print db_management('collection_names')
