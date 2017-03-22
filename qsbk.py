# _*_coding:utf-8 _*_
import urllib2

import re

print '你好'

page=2
url='http://www.qiushibaike.com/8hr/page/'+str(page)

user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
headers={'User-Agent':user_agent}

try:
    #urllib2.Request(url[, data][, headers][,
    # origin_req_host][, unverifiable])
    #rquest类是关于url的一个抽象类,url应该是包含有效url地址的字符串
    # urlopen打开一个request对象
    request=urllib2.Request(url,headers=headers)
    response=urllib2.urlopen(request)
    content=response.read().decode('utf-8')

    #正则表达式匹配
    #.* ? 是一个固定的搭配，.和 * 代表可以匹配任意无限多个字符，加上？表示使用非贪婪模式进行匹配，也就是我们会尽可能短地做匹配，以后我们还会大量用到. *? 的搭配。
    #(. *?)代表一个分组，在这个正则表达式中我们匹配了五个分组，在后面的遍历item中，item[0]
    #re.S标志代表在匹配时为点任意匹配模式，点.也可以代表换行符。
    pattern=re.compile('<div class="article.*?<h2>(.*?)</h2>.*?'
                       +'content">(.*?)</div>.*?stats">.*?number">(.*?)</i>.*?</div>',re.S);

    items=re.findall(pattern,content)
    for item in items:
        print item[0],item[1],item[2]
except urllib2.URLError,e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
