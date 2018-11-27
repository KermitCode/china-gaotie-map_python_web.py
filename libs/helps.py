#!/usr/bin/python
#coding=utf-8

from hashlib import sha1
import sys
import re

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

#get data from input get/post
def param(data, key, default='', isint=False):
    value = data.get(key, default) 
    value = value.strip()
    if isint:
        if value.isdigit():
            return int(value)
        else:
            return 0
    return value 

def shachar(str):
    sh = sha1()
    sh.update(str.encode())
    return sh.hexdigest()

def addtwodimdict(thedict, key_a, key_b, val): 
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})

def htmlshow(data):
    char = """<html lang="zh-CN">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>调试</title>
<style type='text/css'>
table.dataintable {
  margin-top:15px;
  border-collapse:collapse;
  border:1px solid #aaa;
  width:60%;
}
table.dataintable th {
  vertical-align:baseline;
  padding:5px 15px 5px 6px;
  background-color:#3F3F3F;
  border:1px solid #3F3F3F;
  text-align:left;
  color:#fff;
}
table.dataintable td {
  vertical-align:text-top;
  padding:6px 15px 6px 6px;
  border:1px solid #aaa;
}
table.dataintable tr:nth-child(odd) {
  background-color:#F5F5F5;
}
table.dataintable tr:nth-child(even) {
  background-color:#fff;
}
</style>
<body><table class='dataintable'><th>键</th><th>值</th>"""
    for key in data:
       char = char + '<tr><td>'+ key+':</td><td>'+str(data[key])+'</td></tr>'
    return char + '</table></body></html>'

def filter_tags(htmlstr):
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s

def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ','lt':'<','60':'<', 'gt':'>','62':'>', 'amp':'&','38':'&', 'quot':'"','34':'"'}
    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如>
        key=sz.group('name')#去除&;后entity,如>为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr
def repalce(s,re_exp,repl_string):
    return re_exp.sub(repl_string,s)
if __name__=='__main__':
    s=file('169it.com_index.htm').read()
    news=filter_tags(s)
    print news

def goback():
    return """
<html lang="zh-CN">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script>alert('操作成功.');window.location.href = document.referrer;</script>
</head>
</html>
"""
