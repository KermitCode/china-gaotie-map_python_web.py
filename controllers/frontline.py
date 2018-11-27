#!/usr/bin/python
#coding=utf8

#import Init 
import sys
import web 
import re

sys.path.append('../')
from config import conf 
from libs import helps
from models import mysql
import init 

web.config.debug = conf.web_debug

class Gtline:
    def GET(self, linename=''):
        if(linename == ''):
            raise web.seeother('/')
        
        line = mysql.conn.select('gt_line', where={'keychar':linename})
        if(not line):
            raise web.seeother('/')
        linearr,statarr = mysql.getlinearr()

        line = line[0]
        rs = mysql.conn.query("select gl.id,gt.statchar,gt.island,gt.line,province,city,cid,station,stat_id,gl.line_id,img,ga.detail from gt_linestats gl left join gt_station gt on gl.stat_id = gt.id left join gt_citys gc on gt.cid = gc.id left join gt_statimg gsimg on gsimg.zid = gl.stat_id and gsimg.ismain=1 left join gt_article ga on ga.typeval=8 and ga.station_id=gl.stat_id where gl.line_id = %s order by gl.sort asc,gl.id asc,gsimg.ismain desc" % line.id)
        rsnew = []
        for row in rs:
            #row['detail'] = helps.filter_tags(row['detail'])
            dr = re.compile(r'<[^>]+>',re.S)
            dd = dr.sub('', str(row.detail))
            dd = dd.replace('&nbsp;','')
            dd = dd.strip()
            row['detail'] = dd.decode('utf8')[0:200].encode('utf8') + '...'
            rsnew.append(row)
            
        base = init.gettitle()
        return init.frender.line(line, rsnew, linearr,statarr, base)


class Gtlinenew:
    def GET(self, linename=''):
        if(linename == ''):
            raise web.seeother('/')
        
        line = mysql.conn.select('gt_line', where={'keychar':linename})
        if(not line):
            raise web.seeother('/')

        line = line[0]
        #return helps.htmlshow(line)
        line_id = line['id']
        stats = mysql.conn.query("select stat_name,jingweidu from gt_fullstats gf where gf.line_id = %s order by gf.sortnum asc,gf.id asc" % line_id)
        linestatarr = {}
        linearr = {}
        if (len(stats)>1):
            linestatarr[str(line.id)] = stats
            linearr[str(line.id)] = line
        base = init.gettitle()
        #return helps.htmlshow(linestatarr['1'])
        speed = str(line['speed'])
        line_id = str(line_id)
        linestats = linestatarr 
        return init.allrender.everygaotie(linearr, linestatarr, linestats, base, line, speed, line_id) 
