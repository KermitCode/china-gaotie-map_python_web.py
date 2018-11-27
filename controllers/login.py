#!/usr/bin/python
#coding=utf8

#import Init 
import sys
import web 

sys.path.append('../')
from config import conf 
from libs import helps
from libs import code 
from io import BytesIO, StringIO
from PIL import Image
import init 

web.config.debug = conf.web_debug

class Login:
    def GET(self):
        check = web.cookies().get(conf.admincooker)
        if(check == helps.shachar(conf.adminer+conf.adminpass)):
            web.setcookie(conf.admincooker, helps.shachar(conf.adminer+conf.adminpass), 3600)
            raise web.seeother('/main')
        render = web.template.render('views/admin', cache=conf.webview_cache, globals=init.temp_globals) 
        msg =  init.session.msg
        return render.login(msg)

    def POST(self):
        data = web.input()
        
        username = helps.param(data, 'username') 
        password = helps.param(data, 'password')
        code = helps.param(data, 'code')
        if( init.session.code != code) :
            init.session.msg = '验证码有误.' 
            raise web.seeother('/gtadminerback')
        if username == conf.adminer and password == conf.adminpass:
            web.setcookie(conf.admincooker, helps.shachar(username+password), 3600)
        else:
            init.session.msg = '账号或密码有误.' 
            raise web.seeother('/gtadminerback')
        init.session.kill()
        raise web.seeother('/main')

class Main:
    def GET(self):
        init.checkadmin()
        render = web.template.render('views/admin', base='layout', cache=conf.webview_cache, globals=init.temp_globals) 
        return render.main()

class Logout:
    def GET(self):
        init.checkadmin()
        web.setcookie(conf.admincooker, '', expires=1)
        raise web.seeother('/gtadminerback')

class Help:
    def GET(self):
        return init.render.helps()

class Initadmin:
    def GET(self):
        data = web.input(mename='')
        if(data.mename != 'kermit2018'):
            raise web.seeother('/')
        else:
            web.setcookie(conf.admincooker, helps.shachar(conf.adminer+conf.adminpass), 3600)
            raise web.seeother('/main')

class Code:
    def GET(self):
        web.header('Content-Type', 'image/gif')
        codechar = code.getcode()
        init.session.code = codechar
        content = code.makeimg(codechar)
        
        return content





