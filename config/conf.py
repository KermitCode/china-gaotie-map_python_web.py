#!/usr/bin/python
#coding=utf8

import web

#web.py debug state
web_debug = False

#web.py view cache state
webview_cache = False

#project config
project = {
    'name' : '高铁大全管理后台',
}

#admin
adminer = 'test'    
adminpass = 'test'    
admincooker = 'test'

#mysql config
mysqldb = ("127.0.0.1", "user", "pass", "database")

grade=('特等站','一等站','二等站','三等站','四等站','五等站')

status=('已建成','在建','论证中')

typearr=[
    {'id':'1','name':'高铁建设进度'},
    {'id':'2','name':'高铁知识'},
    {'id':'8','name':'高铁站介绍'},
    {'id':'9','name':'高铁线路介绍'}
]

