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

class Index:
    def GET(self):
        lines = mysql.conn.query("select id,name,keychar,statusc,speed,longkm,color from gt_line order by id asc")
        statarr = {}
        linearr = {}
        for line in lines:
            stats = mysql.conn.query("select gt.* from gt_linestats gl left join gt_station gt on gl.stat_id = gt.id  where gl.line_id = %s order by gl.sort asc,gl.id asc" % line.id)
            if (len(stats)>1):
                statarr[str(line.id)] = stats
                linearr[str(line.id)] = line
        base = init.gettitle()
        return init.frender.index(linearr, statarr, base) 

class Chinagaotie:
    def GET(self):
        lines = mysql.conn.query("select id,name,keychar,statusc,speed,longkm,color from gt_line order by id desc")
        linestatarr = {}
        linearr = {}
        for line in lines:
            stats = mysql.conn.query("select stat_name,jingweidu from gt_fullstats gf where gf.line_id = %s order by gf.sortnum asc,gf.id asc" % line.id)
            if (len(stats)>1):
                linestatarr[str(line.id)] = stats
                linearr[str(line.id)] = line
        base = init.gettitles()
        #return helps.htmlshow(linearr)
        return init.allrender.allgaotie(linearr, linestatarr, base) 
