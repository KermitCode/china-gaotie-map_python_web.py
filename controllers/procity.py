#!/usr/bin/python
#coding=utf8

#import Init 
import sys
import web 

sys.path.append('../')
from config import conf 
from libs import helps
from models import mysql
import init 

web.config.debug = conf.web_debug

class Province:
    def GET(self):
        init.checkadmin()
        rs = mysql.conn.select('gt_province', order = 'sort asc')
        return init.render.province(rs)

class City:
    def GET(self):
        init.checkadmin()
        province = mysql.getproArr() 
        get = web.input(proid='1000')
        proid = get.proid
        if(not proid.isdigit() or proid == '0'):
            proid='1000'
        rs = mysql.conn.select('gt_citys', where="proid="+proid, order = 'id asc')
        if(len(rs) <1 ):
            return init.render.error('参数有误')
        proid = int(proid)
        return init.render.city(rs, province, proid)
