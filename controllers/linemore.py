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

class Lineimg:
    def GET(self, lid='0'):
        init.checkadmin()
        if( not lid.isdigit()):
            raise seeother('/')
        rs = mysql.conn.select('gt_line', where="id="+lid)
        if(len(rs) <1 ):
            return seeother('/')
        rs=rs[0]

        data = web.input(delimg='0', mainimg='0');
        delimg = data.delimg
        mainimg = data.mainimg
        #delimg:
        if(delimg != '0'):
            if(not init.checkadmin() and rs.locking == 1):
                return init.render.error('您不能修改已有图片!')
            mysql.conn.delete('gt_lineimg', where="lid=" + lid + " and id=" + delimg)

        #mainimg:
        if(mainimg != '0'):
            if(not init.checkadmin() and rs.locking == 1):
                return init.render.error('您不能修改已有图片!')
            mysql.conn.update('gt_lineimg', where="lid=" + lid, ismain=0)
            mysql.conn.update('gt_lineimg', where="lid=" + lid + " and id=" + mainimg, ismain=1)

        imgs = mysql.conn.select('gt_lineimg', where="lid=" + lid, order="id asc")
        return init.render.lineimg(rs, imgs)
    
    def POST(self, lid='0'):
        init.checkadmin()
        if( not lid.isdigit()):
            return init.jsonerr('invalid line id')
        rs = mysql.conn.select('gt_line', where="id="+lid)
        if(len(rs) <1 ):
            return init.jsonerr('error line id')
        data = web.input(imgurl= '', imgtext = '', imgid='0')
        imgurl = data.imgurl
        imgtext = data.imgtext
        imgid = data.imgid
        if( imgurl != ''):
            sql = "insert ignore into gt_lineimg(lid,img) values(%s, '%s')" % (lid, imgurl)
            rsa = mysql.conn.query(sql)
            if rsa:
                return init.jsonok([], '操作成功')
            else:
                return init.jsonerr('图片已插入，请不要重复图片.')
        
        if( imgtext != ''):
            imgid = imgid.split('_')
            imgid = imgid[-1]
            if(not init.checkadmin() and rs.locking == 1):
                return init.render.error('您不能修改已有图片!')
            mysql.conn.update('gt_lineimg', where="lid=" + lid + " and id="+imgid, says=imgtext)
            return init.jsonok([], '描述添加成功')

        return init.jsonerr('无效操作')

class Linestats:
    def GET(self, lid='0'):
        init.checkadmin()
        data = {}
        data['statarr']= mysql.getstatArr()
        line = mysql.conn.select("gt_line", where="id= " + lid)
        if(len(line) <1 ):
            return init.render.error('id参数有误') 
        line = line[0]
        rs = mysql.conn.query("select gl.id,province,city,cid,station,stat_id,line_id from gt_linestats gl left join gt_station gt on gl.stat_id = gt.id left join gt_citys gc on gt.cid = gc.id where gl.line_id = %s order by gl.sort asc,gl.id asc" % lid)
        return init.render.linestats(line, rs, data)


    def POST(self, lid='0'):
        adminer = init.checkadmin()
        line = mysql.conn.select("gt_line", where="id= " + lid)
        if(len(line) <1 ):
            return init.jsonerr('无效参数')
        
        linedata = line[0]
        if (not adminer and linedata.locking == 1):
            return init.jsonerr('此线路已经完善，不能再编辑.')

        indata = web.input()
        sid = indata.get('sid', '0')
        if(not sid.isdigit() or sid == '0' ):
            return init.jsonerr('无效参数sid')


        #do sort
        sort = indata.get('sort', '0')
        if(sort.isdigit() and sort !='0'):
            rs = mysql.conn.select("gt_linestats", order="sort asc,id asc",where="line_id="+lid)             
            index = 0 
            sort = int(sort)
            for row in rs:
                if(row.id == int(sid)):
                    continue
                index+=1
                if(index == sort):
                    mysql.conn.update("gt_linestats", where="id="+sid, sort = index)  
                    index+=1
                mysql.conn.update("gt_linestats", where="id="+str(row.id), sort = index)  
            return init.jsonok('顺序调整完成')

        station = mysql.conn.select("gt_station", where="id= " + sid)
        if(len(station) <1 ):
            return init.jsonerr('无效参数') 

        mysql.conn.query("insert ignore into gt_linestats(line_id, stat_id) values(%s, %s)" % (lid, sid))
        return init.jsonok('添加成功')
                



