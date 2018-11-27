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

class Gtstation:
    def GET(self, station=''):
        if(station == ''):
            raise web.seeother('/')
        
        stat = mysql.conn.select('gt_station', where={'keychar':station})
        if(not stat):
            raise web.seeother('/')
        return stat.statchar


class Allstation:
    def GET(self):
        rs = mysql.conn.query("select gs.*,gsi.img from gt_statimg gsi left join gt_station gs on gsi.zid=gs.id order by zid asc,gsi.ismain desc")
        base = init.gettitle()
        linearr,statarr = mysql.getlinearr()
        return init.frender.allstation(linearr, statarr, base, rs) 
        

