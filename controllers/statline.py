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

class Station:
    def GET(self):
        adminer = init.checkadmin(False)

        province = mysql.getproArr() 
        get = web.input(proid='0')
        proid = get.proid
        if(not proid.isdigit() or proid == '0'):
            rs = mysql.conn.select('gt_station', order = 'id asc')
        else:
            rs = mysql.conn.select('gt_station', where="pid="+proid, order = 'id asc')
        proid = int(proid) 
        return init.render.station(rs, adminer, proid, province)

class Stationedit:
    def GET(self):
        init.checkadmin()
        data = {}
        data['province'] = mysql.getproArr() 
        data['city'] = mysql.getcityArr() 
        data['cityj'] = json.dumps(data['city'], ensure_ascii=False)
        data['cityjson'] = data['cityj'] #.replace("&quot;",'"');
        data['grade'] = conf.grade
        #modify
        indata = web.input(id='0')
        if(indata.id.isdigit() and indata.id != '0'):
            oridata = mysql.conn.select('gt_station', where="id="+indata.id)
            if(len(oridata) <1 ):
                return init.render.error('id参数有误') 
            oridata = oridata[0]
        else:
            id='0'
            oridata= web.Storage()
        return init.render.stationedit(data, oridata)

    def POST(self):
        init.checkadmin()
        data = web.input()
        line = int(data.line) 
        island = int(data.island) 
        area = int(data.area) 
        keychar = data.statchar.lower().replace(' ', '')

        id = data.get('id', '0')
        #return id
        if(id == '0'):
            mysql.conn.insert('gt_station', pid=data.pid, keychar=keychar, cid=data.cid, station=data.station, statchar=data.statchar, grade=data.grade, address=data.address, longitude=data.longitude, latitude=data.latitude, line=line, island=island, area=area, building=data.building, passengers=data.passengers)
        else:
            rs = mysql.conn.select('gt_station', where="id="+id)
            if(not len(rs)):
                return init.render.error('参数有误!')
            rs =rs[0]
            if(not init.checkadmin() and rs.locking==1):
                return init.render.error('您不能修改已有内容!')
            mysql.conn.update('gt_station', where='id = $id', vars = locals(), keychar=keychar, pid=data.pid, cid=data.cid, station=data.station, statchar=data.statchar, grade=data.grade, address=data.address, longitude=data.longitude, latitude=data.latitude, line=line, island=island, area=area, building=data.building, passengers=data.passengers)
            
        raise web.seeother('/station');
        pass

class Statcheck():
    def POST(self):
        indata = web.input(stat='')
        rs = mysql.conn.select('gt_station', where={'station':indata.stat})
        if(len(rs)):
            return init.jsonerr('此站点已经存在!') 
        else:
            return init.jsonok('可添加')

class Linecheck():
    def POST(self):
        indata = web.input(linename='')
        rs = mysql.conn.select('gt_line', where={'name':indata.linename})
        if(len(rs)):
            return init.jsonerr('此线路已经存在!') 
        else:
            return init.jsonok('可添加')

class Line:
    def GET(self):
        adminer = init.checkadmin(False)
        rs = mysql.conn.select('gt_line', order = 'id asc')
        return init.render.line(rs, adminer)

class Linedit:
    def GET(self):
        init.checkadmin()
        data = {}
        data['status'] = conf.status
        #modify
        indata = web.input(id='0')
        if(indata.id.isdigit() and indata.id != '0'):
            oridata = mysql.conn.select('gt_line', where="id="+indata.id)
            if(len(oridata) <1 ):
                return init.render.error('id参数有误') 
            oridata = oridata[0]
        else:
            id='0'
            oridata= web.Storage()
        return init.render.linedit(data, oridata)

    def POST(self):
        init.checkadmin()
        data = web.input()

        longkm = int(data.longkm)
        speed = int(data.speed) 
        onspeed = int(data.onspeed) 
        keychar = data.namechar.lower().replace(' ', '')

        id = data.get('id', '0')
        #return id
        if(id == '0'):
            mysql.conn.insert('gt_line', keychar=keychar, name=data.name, fullname=data.fullname, namechar=data.namechar, statusc=data.statusc, speed=speed, building=data.building, longkm=longkm, onspeed=onspeed, color=data.color)
        else:
            rs = mysql.conn.select('gt_line', where="id="+id)
            if(not len(rs)):
                return init.render.error('参数有误!') 
            rs = rs[0]
            if(not init.checkadmin() and rs.locking==1):
                return init.render.error('您不能修改已有内容!')
            mysql.conn.update('gt_line', where='id = $id', vars = locals(), keychar=keychar, name=data.name, fullname=data.fullname, namechar=data.namechar, statusc=data.statusc, speed=speed, building=data.building, longkm=longkm, onspeed=onspeed,color=data.color)
        raise web.seeother('/line');
        pass
