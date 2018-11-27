#!/usr/bin/python
#coding=utf8

#import Init 
import sys
import web 
import json
import uniout

sys.path.append('../')
from config import conf 
from libs import helps
from models import mysql
import init 

web.config.debug = conf.web_debug

class Statlock:
    def GET(self):
        adminer = init.checkadmin(False)
        if( not adminer):
            return init.render.error('您无权限操作此项.')

        data = web.input(doid='0');
        doid = data.doid

        if(not doid.isdigit()):
            return init.render.error('参数错误.')
            
        rs = mysql.conn.select('gt_station', where="id="+doid)
        if(not len(rs)): 
            return init.render.error('参数错误.')

        rs=rs[0]
        if(rs.locking == 0):
            locking = '1'
        else:
            locking = '0'
        mysql.conn.update('gt_station', where="id=" +doid, locking=locking)
        return helps.goback()

    
class Linelock:
    def GET(self):
        adminer = init.checkadmin(False)
        if( not adminer):
            return init.render.error('您无权限操作此项.')

        data = web.input(doid='0');
        doid = data.doid

        if(not doid.isdigit()):
            return init.render.error('参数错误.')
            
        rs = mysql.conn.select('gt_line', where="id="+doid)
        if(not len(rs)): 
            return init.render.error('参数错误.')

        rs=rs[0]
        if(rs.locking == 0):
            locking = '1'
        else:
            locking = '0'
        mysql.conn.update('gt_line', where="id=" +doid, locking=locking)
        return helps.goback()

class Artilock:
    def GET(self):
        adminer = init.checkadmin(False)
        if( not adminer):
            return init.render.error('您无权限操作此项.')

        data = web.input(doid='0');
        doid = data.doid

        if(not doid.isdigit()):
            return init.render.error('参数错误.')
            
        rs = mysql.conn.select('gt_article', where="id="+doid)
        if(not len(rs)): 
            return init.render.error('参数错误.')

        rs=rs[0]
        if(rs.locking == 0):
            locking = '1'
        else:
            locking = '0'
        mysql.conn.update('gt_article', where="id=" +doid, locking=locking)
        return helps.goback()
