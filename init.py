#!/usr/bin/python
#coding=utf8

import web 
from config import conf
from libs import helps
import json
from controllers.login import Login, Logout, Main, Code, Help,Initadmin
from controllers.procity import Province, City
from controllers.statline import Station, Stationedit, Line, Linedit, Statcheck, Linecheck 
from controllers.statmore import Stationimg
from controllers.linemore import Lineimg, Linestats 
from controllers.article import Article, Articledit 
from controllers.adminmore import Linelock, Statlock, Artilock 
from controllers.allstatedit import Allstatedit, Getjwd

#front controller
from controllers.frontindex import Index, Chinagaotie
from controllers.frontstation import Gtstation, Allstation 
from controllers.frontline import Gtline, Gtlinenew

#base init values
temp_globals = {
    "datestr" : web.datestr,
    "cookie"  : web.cookies,
    'project' : conf.project,
}

urls = (
    '/', 'Index',
    '/gaotieline/([-\w]+)', 'Gtline',
    '/gaotiestation/([-\w]+)', 'Gtstation',
    '/allstation', 'Allstation',
    '/zhongguo-gaotie-zongtu.zhongguo.gaotie.wang.com', 'Chinagaotie',
    '/zhongguo-gaotie-xianlu/([-\w]+)', 'Gtlinenew',

    #back
    '/gtadminerback', 'Login',
    '/main', 'Main',
    '/initadminfromself', 'Initadmin',
    '/logout', 'Logout',
    '/code', 'Code',
    '/province', 'Province',
    '/city', 'City',
    '/station', 'Station',
    '/stationedit', 'Stationedit',
    '/stationimg/(\d+)', 'Stationimg',
    '/stationtext/(\d+)', 'Stationtext',
    '/line', 'Line',
    '/linedit', 'Linedit',
    '/lineimg/(\d+)', 'Lineimg',
    '/linetext/(\d+)', 'Linetext',
    '/linestats/(\d+)', 'Linestats',
    '/article/(\d+)', 'Article',
    '/articledit', 'Articledit',
    '/help', 'Help',
    '/statlock', 'Statlock',
    '/linelock', 'Linelock',
    '/statcheck', 'Statcheck',
    '/linecheck', 'Linecheck',
    '/allstatedit/(\d+)', 'Allstatedit',
    '/getjwd', 'Getjwd',
    '/artilock', 'Artilock'
)

web.config.debug = conf.web_debug
app = web.application(urls, globals())
render = web.template.render('views/admin', base='layout', cache=conf.webview_cache, globals=temp_globals)
frender = web.template.render('views', base='layout', cache=conf.webview_cache, globals=temp_globals)
allrender = web.template.render('views', base='layout_all', cache=conf.webview_cache, globals=temp_globals)

web.config.session_parameters['cookie_name'] = 'gaotie_adminer'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 300, 
web.config.session_parameters['ignore_expiry'] = False 
web.config.session_parameters['ignore_change_ip'] = False 
web.config.session_parameters['secret_key'] = 'ar9rekjr9e23kj32'
web.config.session_parameters['expired_message'] = 'Session expired'

session = web.session.Session(app, web.session.DiskStore('cache'), initializer={'code': '', 'msg' :''})

#global functions
def checkadmin(refresh=True):
    check = web.cookies().get(conf.admincooker)  
    if(check != helps.shachar(conf.adminer+conf.adminpass)):
        return False
        #raise web.seeother('/gtadminerback')
    else:
        if(refresh is True):
            web.setcookie(conf.admincooker, helps.shachar(conf.adminer+conf.adminpass), 3600)
        return True

def jsonok(data, msg=''):
    rs = {
        'status':'0',
        'msg':msg,
        'data': data
    }
    return json.dumps(rs)

def jsonerr(msg):
    rs = {
        'status':'1',
        'msg':msg,
        'data': [] 
    }
    return json.dumps(rs)

def gettitle():
    titles = {
    'title':'中国高铁线路网总图-中国高速铁路动态线路网总图-中国高铁线路实时更新-中国高铁线网总图',
    'keyword':'高铁,中国高铁,高铁线路,中国高铁线路总网,中国高铁线路总图,中国高铁线路总线网图,中国高速铁路线路规划图,实时更新中国高速铁路图',
    'description':'中国高铁线路网总图,是一个在线生成中国高铁线路网总图的网站，能根据各高铁线路各站点的经纬度数据动态在中国地图上精确地展示中国高速铁路线路的走向，通过动态编辑来实现高铁线路图的动态变更，非常直观形象。作为一个高铁爱好者，对祖国高铁的进步感到由衷的高兴，为了能实时查看最新的高铁线路，开发了此小站，欢迎有相同爱好的朋友加QQ群：827667455'
    }
    return titles


def gettitles():
    titles = {
    'title':'中国高铁地图-中国高铁线路图-中国所有高铁线路地图-中国全部高铁地图-中国所有高铁汇总-中国全部高铁-中国高铁汇总',
    'keyword':'中国高铁地图,中国高铁线路图,中国所有高铁线路地图,中国全部高铁地图,中国所有高铁汇总,国全部高铁,中国高铁汇总',
    'description':'中国高铁线路网总图,是一个在线生成中国高铁线路网总图的网站，能根据各高铁线路各站点的经纬度数据动态在中国地图上精确地展示中国高速铁路线路的走向，通过动态编辑来实现高铁线路图的动态变更，非常直观形象。作为一个高铁爱好者，对祖国高铁的进步感到由衷的高兴，为了能实时查看最新的高铁线路，开发了此小站，欢迎有相同爱好的朋友加QQ群：827667455'
    }
    return titles




