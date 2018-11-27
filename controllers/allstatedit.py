#!/usr/bin/python
#coding=utf8

#import Init 
import sys
import web 
import json
import uniout
import urllib2

sys.path.append('../')
from config import conf 
from libs import helps
from models import mysql
import init 

web.config.debug = conf.web_debug

class Allstatedit:
    def GET(self, lid='0'):
        rs=init.checkadmin()
        if not rs:
            raise web.seeother('/')
        if( not lid.isdigit()):
            raise seeother('/')
        rs = mysql.conn.select('gt_line', where="id="+lid)
        if(len(rs) <1 ):
            return seeother('/')
        rs=rs[0]
        #return helps.htmlshow(rs)
    
        #get all stations
        sql = "select * from gt_fullstats where line_id='%s' order by sortnum asc,id asc" % lid
        oridata = mysql.conn.query(sql)
        web.header("Access-Control-Allow-Origin", "*")
        return init.render.allstatedit(rs, oridata, lid)

    def POST(self, lid='0'):
        rs=init.checkadmin()
        if not rs:
            raise web.seeother('/')
        if( not lid.isdigit()):
            raise seeother('/')
        rs = mysql.conn.select('gt_line', where="id="+lid)
        if(len(rs) <1 ):
            return seeother('/')

        #do stat data
        rs=rs[0]
        data = web.input()
        #return helps.htmlshow(data);
        test=[]
        for num in range(1, 200):
            i = str(num) 
            stat=data.get("st_"+i, '')
            stat=stat.strip()
            if not stat:
                sql = "delete from gt_fullstats where line_id=%s and sortnum > %s" % (lid, i)
                rs = mysql.conn.query(sql)
                break;
            else:
                sortv = data.get("s_"+i, '1000')
                jwd = data.get("jwd_"+i, '116.400819,39.92556')
                sortv = sortv.strip()
                jwd = jwd.strip()
                web.header('Content-Type', 'text/html;charset=UTF-8')
                
                #return sortv+stat+jwd
                sql="insert ignore into gt_fullstats(line_id,stat_name,jingweidu,sortnum) values('%s','%s','%s','%s') ON DUPLICATE KEY UPDATE jingweidu='%s',sortnum='%s'" % (lid,stat,jwd,sortv,jwd,sortv)
                rs = mysql.conn.query(sql)
                #return sql
                
        raise web.seeother('/allstatedit/'+lid);
        pass

class Getjwd:
    def GET(self):
        get = web.input(stat='')
        stat = get.stat
        if(stat != ''):
            rs = mysql.conn.select('gt_fullstats', where="stat_name='"+stat+"'", order = 'id asc', limit =1)
            if len(rs):
                return rs[0]['jingweidu']
        url="http://api.map.baidu.com/geocoder?output=json&key=573eb860166f9e68b008627e95c8d496&city=&address="+stat
        req = urllib2.Request(url)
        cont = urllib2.urlopen(req)
        cont = cont.read()
        hjson = json.loads(cont)
        return str(hjson['result']['location']['lng'])+','+ str(hjson['result']['location']['lat'])





