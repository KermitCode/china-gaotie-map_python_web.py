#!/usr/bin/python
#coding=utf8

import web
import sys
import datetime

sys.path.append('../')
from config import conf
from libs import helps

conn = web.database(dbn = 'mysql', db = conf.mysqldb[3], user = conf.mysqldb[1], pw = conf.mysqldb[2], host = conf.mysqldb[0])

def getproArr():
    data = conn.select('gt_province', order = 'sort asc')
    arr = [] 
    for row in data:
        arr.append({'id':row['id'], 'pro':row['province']})
    return arr
  
def getcityArr():
    data = conn.query("select proid,id,city from gt_citys order by id asc")
    arr = dict() 
    for row in data:
       helps.addtwodimdict(arr, row['proid'], row['id'], row['city'])
    return arr

def getlineArr():
    data = conn.select('gt_line', order = 'id asc')
    arr = [] 
    for row in data:
        arr.append({'lid':row['id'], 'name':row['name']+'--'+row['fullname']+'--'+ str(row['speed'])+'km/h'})
    return arr

def getstatArr():
    sql = "select gs.id, gs.station, gp.province from gt_station gs left join gt_province gp on gp.id=gs.pid order by gp.sort asc,gs.id asc"
    data = conn.query(sql)
    arr = dict() 
    for row in data:
        helps.addtwodimdict(arr, row['province'], row['id'], row['station'])
    return arr
#def new_post(title, text):
# db.insert('entries',
#  title = title,
#  content = text,
#  posted_on = datetime.datetime.utcnow())


def getlinearr():
    lines = conn.query("select id,name,keychar,statusc,speed,longkm,color from gt_line order by id asc")
    statarr = {}
    linearr = {}
    for line in lines:
        stats = conn.query("select gt.* from gt_linestats gl left join gt_station gt on gl.stat_id = gt.id  where gl.line_id = %s order by gl.sort asc,gl.id asc" % line.id)
        if (len(stats)>1):
            statarr[str(line.id)] = stats
            linearr[str(line.id)] = line        
    return linearr,statarr

