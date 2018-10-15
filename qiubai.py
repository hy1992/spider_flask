# -*- coding:utf-8 -*-
import requests
from lxml import etree
from threading import Thread
from time import sleep
import re

class QbSpider:
    def __init__(self):
        self.baseurl = "https://www.qiushibaike.com"
        self.url = "https://www.qiushibaike.com/hot/page/"
        self.pn = 1
        self.headers = {"User-Agent": "Mozilla5.0/"}

    def getPage(self,url):
        res = requests.get(url,headers=self.headers)
        res.encoding = 'utf-8'
        return res.text
    def parsePage(self,html):
        parseHtml = etree.HTML(html)
        r_list = parseHtml.xpath('//div[@id="content-left"]/div/a/@href')
        url_list = []
        for i in r_list:
            if i:
                url_list.append(self.baseurl+i.strip())
        url_list = list(set(url_list))
        return url_list
    def getContent(self,r_list):
        L = []
        for url in r_list:
            res = requests.get(url,headers=self.headers)
            sleep(0.1)
            res.encoding = 'utf-8'
            html = res.text
            parsrHtml = etree.HTML(html)
            username = parsrHtml.xpath('//div[@class="author clearfix"]/a/h2')
            pattern = re.compile('<div class="content">([\s\S]+?)</div>')
            content = pattern.findall(html)
            # content = parsrHtml.xpath('//div[@id="single-next-link"]/div[@class="content"]')
            if username:
                d = {
                    'username':username[0].text,
                    'content':content[0]
                }
                L.append(d)
        return L
    def workOn(self,p=None):
        c_list = []
        p = int(p)
        while p > self.pn:
            url = self.url + str(self.pn)
            html = self.getPage(url)
            a_list = self.parsePage(html)
            con_list = self.getContent(a_list)
            c_list.extend(con_list)
            self.pn += 1
        print(len(c_list))
        return c_list

if __name__ == "__main__":
    spi = QbSpider()
    l = spi.workOn(2)
    print(l[0])


