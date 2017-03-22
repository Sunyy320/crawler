# _*_coding:utf-8 _*_
import urllib2

import re


class QSBK:
    def __init__(self):
        self.pageIndex=1
        self.user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
        #初始化headers
        self.headers={'User-Agent':self.user_agent}
        #存放段子打变量，每一个元素是每一页的段子们
        self.stories=[]
        #存放程序是否继续进行的变量
        self.enable=False

     #传入某一页的页数，获取该页代码
    def getPage(self,pageIndex):
            try:
                url = 'http://www.qiushibaike.com/8hr/page/' + str(pageIndex)
                request = urllib2.Request(url, headers=self.headers)
                response = urllib2.urlopen(request)
                content=response.read().decode('utf-8')
                return  content
            except urllib2.URLError,e:
                if hasattr(e,"reason"):
                    print u"连接失败，错误原因",e.reason
                    return  None

    #传入某页页码，获取提取内容
    def getPageItems(self,pageIndex):
        pageCode=self.getPage(pageIndex)

        if not pageCode:
            print "页面加载失败。。。。。。"
            return  None
        pattern = re.compile('<div class="article.*?<h2>(.*?)</h2>.*?'
                             + 'content">(.*?)</div>.*?stats">.*?number">(.*?)</i>.*?</div>', re.S);

        items = re.findall(pattern, pageCode)
        pageStories=[]
        for item in items:
            #去除<br/><span></span>标签
            replace=re.compile('<br/>|<span>|</span>')
            text=re.sub(replace,"\n",item[1])
            pageStories.append([item[0].strip(),text.strip(),item[2].strip()])
        return pageStories

    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        if self.enable==True:
            #当前未看页数少于2,则加载新的一页
            if len(self.stories)<2:
                pageStories=self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex+=1

    def getOne(self,pageStories,page):
        for story in pageStories:
            input=raw_input()
            self.loadPage()
            if input=="Q":
                self.enable=False
                return
            print u'第%d页\n作者:%s \n内容:%s \n 好笑人数：%s\n' % (page,story[0],story[1],story[2])

    def start(self):
        print u'正在读取糗事百科，按回车查看新段子，Q退出'
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOne(pageStories, nowPage)

spide=QSBK()
spide.start()
