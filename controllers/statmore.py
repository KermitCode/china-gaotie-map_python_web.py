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

class Stationimg:
    def GET(self, zid='0'):
        init.checkadmin()
        if( not zid.isdigit()):
            raise seeother('/')
        rs = mysql.conn.select('gt_station', where="id="+zid)
        if(len(rs) <1 ):
            return seeother('/')
        rs=rs[0]

        data = web.input(delimg='0', mainimg='0');
        delimg = data.delimg
        mainimg = data.mainimg
        #delimg:
        if(delimg != '0'):
            if(not init.checkadmin() and rs.locking==1):
                return init.render.error('您不能删除已有图片!')
            mysql.conn.delete('gt_statimg', where="zid=" + zid + " and id=" + delimg)

        #mainimg:
        if(mainimg != '0'):
            if(not init.checkadmin() and rs.locking==1):
                return init.render.error('您不能删除已有图片!')
            mysql.conn.update('gt_statimg', where="zid=" + zid, ismain=0)
            mysql.conn.update('gt_statimg', where="zid=" + zid + " and id=" + mainimg, ismain=1)

        imgs = mysql.conn.select('gt_statimg', where="zid=" + zid, order="id asc")
        return init.render.stationimg(rs, imgs)
    
    def POST(self, zid='0'):
        if( not zid.isdigit()):
            return init.jsonerr('invalid zid')
        rs = mysql.conn.select('gt_station', where="id="+zid)
        if(len(rs) <1 ):
            return init.jsonerr('error zid')
        data = web.input(imgurl= '', imgtext = '', imgid='0')
        imgurl = data.imgurl
        imgtext = data.imgtext
        imgid = data.imgid
        if( imgurl != ''):
            sql = "insert ignore into gt_statimg(zid,img) values(%s, '%s')" % (zid, imgurl)
            rs = mysql.conn.query(sql)
            if rs:
                return init.jsonok([], '操作成功')
            else:
                return init.jsonerr('图片已插入，请不要重复图片.')
        
        if( imgtext != ''):
            if(not init.checkadmin() and rs.locking==1):
                return init.render.error('您不能删除已有图片!')
            imgid = imgid.split('_')
            imgid = imgid[-1]
            mysql.conn.update('gt_statimg', where="zid=" + zid + " and id="+imgid, says=imgtext)
            return init.jsonok([], '描述添加成功')

        return init.jsonerr('无效操作')
