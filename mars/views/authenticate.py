#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-10
# @File    : authenticate.py
# @Desc    : ""

from flask import Blueprint, render_template, request, redirect, url_for, Flask, session
from instance import config
from functools import wraps

authenticate = Blueprint('authenticate', __name__)
ProductionConfig = config.ProductionConfig
app = Flask(__name__)
app.config.from_object(ProductionConfig)


@authenticate.route('/login', methods=['GET', 'POST'])
def login_view():
    # login view
    if request.method == 'POST':
        # username = request.form.get('username')
        password = request.form.get('password')
        if password == app.config.get('WEB_PASSWORD'):
            try:
                session['login'] = 'A1akPTQJiz9wi9yo4rDz8ubM1b1'
                return redirect(url_for('index.view_base'))
            except Exception as e:
                print(e)
                return render_template('login.html', msg="Internal Server Error")
        else:
            return render_template('login.html', msg="Invalid Password")
    return render_template('login.html')


# login-out
@authenticate.route('/login-out')
def login_out():
    session['login'] = ''
    return redirect(url_for('authenticate.login_view'))


# login-check
def login_check(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if "login" in session:
                if session['login'] == 'A1akPTQJiz9wi9yo4rDz8ubM1b1':
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for('authenticate.login_view'))
            else:
                return redirect(url_for('authenticate.login_view'))
        except Exception, e:
            print e
            return redirect(url_for('authenticate.login_view'))
    return wrapper
