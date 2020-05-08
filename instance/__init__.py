#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-10
# @File    : __init__.py.py
# @Desc    : ""

from flask import Flask
from instance import config

ProductionConfig = config.ProductionConfig
app = Flask(__name__)
app.config.from_object(ProductionConfig)
config_name = app.config.get('CONFIG_NAME')
