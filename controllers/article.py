#!/usr/bin/python
#coding=utf8

#import Init 
import sys
import web 
import time

sys.path.append('../')
from config import conf 
from libs import helps
from models import mysql
import init 

web.config.debug = conf.web_debug

class Articledit:
    def GET(self):
        init.checkadmin()
        
        indata = web.input()
        aid = indata.get('aid', '0')
        sid = indata.get('sid', '0')
        lid = indata.get('lid', '0')

        if(not aid.isdigit()):
            aid='0'
        if(not sid.isdigit()):
            sid='0'
        if(not lid.isdigit()):
            lid='0'

        oridata = {}
        if(aid !='0' or sid !='0'  or lid !='0' ):
            if(aid !='0' ):
                oridata = mysql.conn.select('gt_article', where="id="+aid)
                if(len(oridata) <1 ):
                    return init.render.error('参数有误')
            elif(sid !='0' ):
                oridata = mysql.conn.select('gt_article', where="station_id="+sid)
            else:
                oridata = mysql.conn.select('gt_article', where="line_id="+lid)
            if(len(oridata) >=1 ):
                oridata = oridata[0]
            else:
                oridata = {}
        data = {}
        data['type'] = conf.typearr
        data['linearr'] = mysql.getlineArr()
        data['statarr']= mysql.getstatArr()
        return init.render.articledit(data, oridata, sid, lid)

    def POST(self):
        init.checkadmin()
        data = web.input()
        id = data.get('id', '0')
        station_id = data.get('station_id', '0');
        if(not station_id.isdigit()):
            station_id = '0'
        line_id = data.get('line_id', '0');
        if(not line_id.isdigit()):
            line_id = '0'
        nowt = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
        #return helps.htmlshow(data) 
        if(id == '0'):
            mysql.conn.insert('gt_article', title=data.title, line_id = line_id,  station_id = station_id, typeval=data.typeval, detail=data.detail, create_time=nowt, update_time=nowt)
        else:
            rs = mysql.conn.select('gt_article', where="id="+id) 
            if(not len(rs)):
                return init.render.error('参数错误!')
            rs = rs[0]
            if(not init.checkadmin() and rs.locking == 1):
                return init.render.error('您不能修改已有内容!')
            mysql.conn.update('gt_article', where="id="+id, title=data.title, line_id = line_id,  station_id = station_id, typeval=data.typeval, detail=data.detail, update_time=nowt)
        raise web.seeother("/article/"+data.typeval)

class Article:
    def GET(self, typeid):
        adminer = init.checkadmin(False)
        find=False
        for item in conf.typearr:
            if(item['id'] ==  typeid):
                find = True
        if(not find):
            return web.seeother('/')
        rs = mysql.conn.select('gt_article', where="typeval="+typeid)
        return init.render.article(rs, adminer)



