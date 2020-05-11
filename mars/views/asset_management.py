#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-10
# @File    : asset_management.py
# @Desc    : ""

import time,re,urllib,os,subprocess
import json
from multiprocessing import Process
from threading import Thread
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from bson import ObjectId
from lib.mongo_db import connectiondb, db_name_conf
from mars.views.authenticate import login_check
from instance import config_name
from mars.views.modules.discovery.asset_discovery import AssetDiscovery

asset_management = Blueprint('asset_management', __name__)
tasks_db = db_name_conf()['tasks_db']
asset_db = db_name_conf()['asset_db']
server_db = db_name_conf()['server_db']
subdomain_db = db_name_conf()['subdomain_db']
vul_db = db_name_conf()['vul_db']
plugin_db = db_name_conf()['plugin_db']
config_db = db_name_conf()['config_db']
cus_db = db_name_conf()['cus_db']



def get_domain(target):
    try:
        url = target
        if url[0:4] == 'http':
            proto, rest = urllib.splittype(url)
            host, rest = urllib.splithost(rest)
            if host[0:3] == 'www':
                host = host[4:]
        elif url[0:3] == 'www':
            host = url[4:]
        else:
            host = url
        if ':' in host:
            host = host.split(':')[0]
        if '/' in host:
            host = host.split('/')[0]

        return host
    except:
        return target

def get_main_domain(domain):
    double_exts = ['.com.cn','.edu.cn','.gov.cn','.org.cn','.net.cn']

    main_domain = domain

    for ext in double_exts:
        if ext in domain:
            if len(domain.split('.')) > 3:
                # print "yuanshi",domain
                domain_split = domain.split('.')
                domain_new = "%s.%s.%s" % (domain_split[-3], domain_split[-2], domain_split[-1])
                # print "exact",domain
                main_domain = domain_new
            else:
                main_domain = domain

            break
        else:
            if len(domain.split('.')) > 2:
                domain_split = domain.split('.')
                domain_new = "%s.%s" % (domain_split[-2], domain_split[-1])
                main_domain = domain_new
            else:
                main_domain = domain
    return main_domain


def ip_regex(raw):
    '''
    Collect legal ip
    1.1.1.1 | 10.1.1.1 | 256.10.1.256 | 222.212.22.11 | 0.0.150.150 | 232.21.234.256
    '''
    ips = []
    try:
        re_ips = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',str(raw))
        for ip in re_ips:
            compile_ip = re.compile(r'^((?:(?:[1-9])|(?:[1-9][0-9])|(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])))(?:\.(?:(?:[0-9])|(?:[1-9][0-9])|(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])))){3})$')
            if compile_ip.match(ip):
                ips.append(ip)
    except Exception,e:
        print e
        pass
    return ips

def start_scan():
    pwd = os.getcwd()
    time.sleep(3)
    os.chdir(pwd +'/taskpython/')
    if connectiondb(asset_db).find({'task_state':'new','discover_option':'Enable'}).count() > 0:
        subprocess.Popen(['python',pwd +"/taskpython/asset_task_scan_v1.0.py"])

# new asset view
@asset_management.route('/new-asset', methods=['GET', 'POST'])
@login_check
def new_asset():
    # default asset view
    if request.method == "GET":
        cus_data = connectiondb(cus_db).find().sort('cus_add_time', 1)
        return render_template('new-asset.html',cus_data=cus_data)
    else:
        # create asset (post)
        if request.form.get("source") == "new_asset":
            # asset_name = request.form.get('asset_name')
            asset_host = request.form.get('asset_host').replace('\r', '').split('\n', -1)  # 返回元组([u'www.vbboy.com', u'demo.tidesec.net', u'http://www.tidesec.net', u'192.168.1.1/24'],)
            asset_cus_tmp = request.form.get('asset_cus_id')
            admin_name = request.form.get('admin_name')
            discover_option = request.form.get('discover_option')
            asset_scan_zhouqi = request.form.get('asset_scan_zhouqi')
            domain_fast_port_scan = request.form.get('domain_fast_port_scan')
            c_scan = request.form.get('c_scan')
            c_fast_port_scan = request.form.get('c_fast_port_scan')

            asset_cus_id = asset_cus_tmp.split('_')[0]
            asset_cus_name = asset_cus_tmp.split('_')[1]

            if discover_option == "true":
                discover_option = 'Enable'
            else:
                discover_option = 'Disallow'

            if domain_fast_port_scan == "true":
                domain_fast_port_scan = 'Enable'
            else:
                domain_fast_port_scan = 'Disable'

            if c_scan == "true":
                c_scan = 'Enable'
            else:
                c_scan = 'Disable'

            if c_fast_port_scan == "true":
                c_fast_port_scan = 'Enable'
            else:
                c_fast_port_scan = 'Disable'

            new_task = {}
            asset_task_tmp = asset_host

            task_add_flag = 1

            for asset_task in asset_task_tmp:
                asset_task = asset_task.strip()
                if ip_regex(asset_task):  # 如果是IP
                    if str(asset_task).startswith('http') or ":" in asset_task:
                        if not new_task.has_key('other_host'):
                            new_task['other_host']=[]
                            new_task['other_host'].append(asset_task)
                        else:
                            new_task['other_host'].append(asset_task)
                    else:
                        if not new_task.has_key(asset_task):
                            new_task[asset_task]=[]
                            new_task[asset_task].append(asset_task)
                        else:
                            new_task[asset_task].append(asset_task)
                else:
                    task_main_domain =get_main_domain(get_domain(asset_task))
                    if new_task.has_key(task_main_domain):
                        new_task[task_main_domain].append(asset_task)
                    else:
                        new_task[task_main_domain]=[]
                        new_task[task_main_domain].append(asset_task)

            # print "new_task",new_task

            for new_task_name in new_task:
                # print new_task[new_task_name]
                asset_data = {
                    'asset_name': new_task_name,
                    'asset_host': new_task[new_task_name],
                    'asset_cus_id': asset_cus_id,
                    'asset_cus_name': asset_cus_name,
                    'admin_name': admin_name,
                    "asset_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'discover_option': discover_option,
                    'task_state':'new',
                    'domain_fast_port_scan':domain_fast_port_scan,
                    'asset_scan_zhouqi':asset_scan_zhouqi,
                    'c_scan':c_scan,
                    'c_fast_port_scan':c_fast_port_scan,

                }
                # print "new_task_name",asset_data

                # # asset_id = 1
                existe_cus_datas = connectiondb(asset_db).find_one({'asset_name':asset_data['asset_name']})
                # print "existe_cus_datas",existe_cus_datas
                if not existe_cus_datas:
                    asset_id = connectiondb(asset_db).insert_one(asset_data).inserted_id
                    if asset_id:
                        task_add_flag = 1
                        # scanner = AssetDiscovery(asset_id)
                        # t1 = Thread(target=scanner.set_discovery, args=())
                        # t1.start()
                    else:
                        task_add_flag = 0
                else:
                    existe_host = []
                    if type(existe_cus_datas['asset_host']) == type([]):
                        existe_host = existe_cus_datas['asset_host']
                    else:
                        existe_host.append(existe_cus_datas['asset_host'])

                    if existe_host:
                        for host in asset_data['asset_host']:
                            existe_host.append(host)
                    else:
                        existe_host = asset_data['asset_host']
                    update_asset = connectiondb(asset_db).update_one(
                        {'_id': ObjectId(existe_cus_datas['_id'])},
                        {'$set': {
                            'asset_host': existe_host,
                            'task_state':'new',
                        }
                        })
                    if update_asset:
                        task_add_flag = 1
                    else:
                        task_add_flag = 0

            if task_add_flag:
                # p = Process(target=start_scan)  # 申请子进程
                # p.start()
                return "success"
            else:
                return "Warning"
        else:
            return "Warning"


# asset view
@asset_management.route('/asset-management', methods=['GET', 'POST'])
@login_check
def asset_view():
    if request.method == "GET":
        # asset delete
        if request.args.get("delete"):
            asset_id = request.args.get("delete")
            if connectiondb(asset_db).delete_one({'_id': ObjectId(asset_id)}):
                if connectiondb(server_db).delete_many({'asset_task_id': asset_id}):
                    return "success"

        elif request.args.get("cus"):
            asset_cus_id = request.args.get("cus")
            asset_info = connectiondb(asset_db).find({'asset_cus_id': asset_cus_id})
            asset_info_tmp = []

            for x in asset_info:
                asset_task_id = str(x['_id'])
                x['asset_server_num'] = connectiondb(server_db).find({'asset_task_id': asset_task_id}).count()
                asset_info_tmp.append(x)

            config_info = connectiondb(config_db).find_one({"config_name": config_name})
            plugin_info = connectiondb(plugin_db).find()
            username_list = '\n'.join(config_info['username_dict'])
            password_list = '\n'.join(config_info['password_dict'])
            protocols = config_info['auth_service']

            return render_template("asset-management.html", asset_info=asset_info_tmp, plugin_info=plugin_info,
                                   protocols=protocols, username_list=username_list, password_list=password_list)

        # get asset info
        elif request.args.get("edit"):
            asset_id = request.args.get("edit")
            try:
                asset_info = connectiondb(asset_db).find_one({'_id': ObjectId(asset_id)})
                asset_info_json = {
                    'asset_name': asset_info['asset_name'],
                    'admin_name': asset_info['admin_name'],
                    'asset_cus_id': asset_info['asset_cus_id'],
                    'task_state': asset_info['task_state'],
                    'discover_option': asset_info['discover_option'],
                    'asset_cus_name': asset_info['asset_cus_name'],
                    'asset_scan_zhouqi': asset_info['asset_scan_zhouqi'],
                    'asset_id': asset_id,
                    'asset_host': '\n'.join(asset_info['asset_host']),
                }
                return jsonify(asset_info_json)
            except Exception as e:
                print(e)

        # get asset host info for new scan
        elif request.args.get("scan"):
            asset_id = request.args.get("scan")
            try:
                asset_host = connectiondb(asset_db).find_one({'_id': ObjectId(asset_id)})['asset_host']
                asset_host_json = {
                    'asset_host': '\n'.join(asset_host),
                }
                return jsonify(asset_host_json)
            except Exception as e:
                print(e)
        else:
            # asset list(view)
            config_info = connectiondb(config_db).find_one({"config_name": config_name})
            asset_info = connectiondb(asset_db).find()

            asset_info_tmp = []

            for x in asset_info:
                asset_task_id = str(x['_id'])
                x['asset_server_num'] = connectiondb(server_db).find({'asset_task_id': asset_task_id}).count()
                asset_info_tmp.append(x)

            # cus_info = connectiondb(cus_db).find()
            #
            # asset_info_tmp = []
            # cus_info_tmp = []
            #
            # for y in cus_info:
            #     cus_info_tmp.append(y)
            #
            # for x in asset_info:
            #     if x.has_key('asset_cus_id'):
            #         for z in cus_info_tmp:
            #             if str(z['_id']) == str(x['asset_cus_id']):
            #                 x['cus_name'] = z['cus_name']
            #                 asset_info_tmp.append(x)

            plugin_info = connectiondb(plugin_db).find()
            username_list = '\n'.join(config_info['username_dict'])
            password_list = '\n'.join(config_info['password_dict'])
            protocols = config_info['auth_service']
            return render_template("asset-management.html", asset_info=asset_info_tmp, plugin_info=plugin_info,
                                   protocols=protocols, username_list=username_list, password_list=password_list)

    else:
        # asset db update
        if request.form.get("source") == "asset_update":
            asset_id = request.form.get('asset_id')
            # asset_name = request.form.get('asset_name')
            # asset_host = request.form.get('host_val').replace('\r', '').split('\n', -1),
            # dept_name = request.form.get('dept_name')
            # admin_name = request.form.get('admin_name')
            # discover_option = request.form.get('discover_option')
            # if discover_option == "true":
            #     discover_option = 'Enable'
            # else:
            #     discover_option = 'Disallow'
            task_state = request.form.get('task_state')
            if task_state == "true":
                task_state = 'new'

                update_asset = connectiondb(asset_db).update_one(
                    {'_id': ObjectId(asset_id)},
                    {'$set': {
                        # 'asset_name': asset_name,
                        # 'dept_name': dept_name,
                        # 'asset_host': asset_host[0],
                        # 'admin_name': admin_name,
                        # "asset_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        'task_state': task_state,
                    }
                    }
                )
                if update_asset:
                    # if discover_option == "Enable":
                    #     scanner = AssetDiscovery(ObjectId(asset_id))
                    #     t1 = Thread(target=scanner.set_discovery, args=())
                    #     t1.start()
                    return "success"
                else:
                    return "Warning"


# asset server view
@asset_management.route('/asset-services', methods=['GET', 'POST'])
@login_check
def asset_server():
    if request.method == "GET":
        plugin_info = connectiondb(plugin_db).find()
        if request.args.get('asset'):
            asset_id = request.args.get('asset')
            server_data = connectiondb(server_db).find({"tag": {"$ne": "delete"}, 'asset_task_id': asset_id})
            return render_template("asset-services.html", server_data=server_data, plugin_info=plugin_info)
        elif request.args.get('cus'):
            asset_cus_id = request.args.get('cus')
            server_data = connectiondb(server_db).find({"tag": {"$ne": "delete"}, 'asset_cus_id': asset_cus_id})
            return render_template("asset-services.html", server_data=server_data, plugin_info=plugin_info)
        elif request.args.get('delete'):
            server_id = request.args.get('delete')
            refer_url = request.referrer
            if connectiondb(server_db).delete_one({'_id': ObjectId(server_id)}):
                return redirect(refer_url)
            # if connectiondb(server_db).update_one({'_id': ObjectId(server_id)}, {"$set": {"tag": "delete"}}):
            #     return redirect(url_for('asset_management.asset_server'))

        elif request.args.get('info'):
            server_id = request.args.get('info')
            server_info = connectiondb(server_db).find_one({"tag": {"$ne": "delete"}, '_id': ObjectId(server_id)})
            if server_info:
                del server_info['_id']
                del server_info['asset_cus_id']
                return jsonify(server_info)
            else:
                return jsonify({"result": "Warning"})

        server_data = connectiondb(server_db).find({"tag": {"$ne": "delete"}})
        return render_template("asset-services.html", server_data=server_data, plugin_info=plugin_info)
    else:
        if request.form.get('source') == 'server_scan':
            server_host = []
            server_list = request.form.get('server_list').split(",")
            for server_id in server_list:
                server_info = connectiondb(server_db).find_one({"_id": ObjectId(server_id)})
                server_host.append(server_info['host'] + ":" + str(server_info['port']))
            return "\n".join(server_host)

# asset info view
@asset_management.route('/asset-info', methods=['GET', 'POST'])
@login_check
def asset_info():
    if request.method == "GET":
        # plugin_info = connectiondb(plugin_db).find()
        if request.args.get('server'):
            server_id = request.args.get('server')
            server_data = connectiondb(server_db).find({'_id': ObjectId(server_id)})
            return render_template("asset-info.html", server_data=server_data)
        elif request.args.get('delete'):
            server_id = request.args.get('delete')
            if connectiondb(server_db).delete_one({'_id': ObjectId(server_id)}):
                return redirect(url_for('asset_management.asset_server'))
        elif request.args.get('port'):
            id_port = request.args.get('port')
            if id_port:
                server_id = id_port.split('_')[0]
                port_id = id_port.split('_')[1]

                server_info = connectiondb(server_db).find_one({"_id": ObjectId(server_id)})
                if server_info:
                    if server_info.has_key('port_info'):
                        for port_tmp in server_info['port_info']:
                            if str(port_tmp['port'])  == port_id:
                                return jsonify(port_tmp)
                else:
                    return jsonify({"result": "Not Found ServerInfo"})

            else:
                return jsonify({"result": "Warning id_port"})
        server_data = connectiondb(server_db).find({"tag": {"$ne": "delete"}})

        return render_template("asset-info.html", server_data=server_data)



@asset_management.route('/search', methods=['GET', 'POST'])
@login_check
def search_view():
    config_info = connectiondb(config_db).find_one({"config_name": config_name})
    username_list = '\n'.join(config_info['username_dict'])
    password_list = '\n'.join(config_info['password_dict'])
    plugin_info = connectiondb(plugin_db).find()
    protocols = config_info['auth_service']
    if request.method == "GET":
        data = "Your search - \"\" - did not match any documents."
        return render_template('search.html', data=data, plugin_info=plugin_info, protocols=protocols)
    else:
        search_result = []
        key = request.form.get('search').strip()
        for i in connectiondb(server_db).find({"tag": {"$ne": "delete"}}, {'_id': 0, 'asset_id': 0}):
            if key in str(i):
                search_result.append(i)
        if len(search_result) == 0:
            data = "Your search - " + key + " - did not match any documents."
            return render_template('search.html', data=data)
        else:
            return render_template('search.html', search_result=search_result, plugin_info=plugin_info,
                                   username_list=username_list, password_list=password_list, protocols=protocols)
