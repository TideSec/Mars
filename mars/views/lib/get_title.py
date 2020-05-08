#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : TideSec
# @Time    : 18-5-21
# @File    : get_title.py
# @Desc    : ""

import requests
import re


class TitleParser:
    def __init__(self, target):
        self.target = target
        self.title = ''

    def parser_title(self):
        try:
            res = requests.get(self.target)
            match = re.search('<title>(.*?)</title>', res.content)
            if match:
                self.title = match.group(1)
            else:
                self.title = 'None'
        except Exception as e:
            self.title = 'ERR_CONNECTION_REFUSED'
        return self.title


def get_title(target, subdomain_id):
    target_url = "http://" + target
    result = {
        "title": TitleParser(target_url).parser_title(),
        "_id": subdomain_id
    }
    return result
