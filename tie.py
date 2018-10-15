# -*- coding:utf-8 -*-
import requests
from lxml import etree
from threading import Thread
from time import sleep
import os

class TiebaSpider:
    def __init__(self):
        self.url = "http://tieba.baidu.com/f?"
        self.baseurl = "http://tieba.baidu.com/"
        self.headers = {"User-Agent": "Mozilla5.0/"}
        self.pn = 0
        self.page = 1
        self.l = []

    def getPage(self, kw, url):
        params = {
            "kw": kw,
            "pn": self.pn
        }
        res = requests.get(url, params=params, headers=self.headers)
        res.encoding = "utf-8"
        return res.text
    def parsePage(self,html):
        parseHtml = etree.HTML(html)
        r_list = parseHtml.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a/@href')
        url_list = []
        for i in r_list:
            url_list.append(self.baseurl + i.strip())
        return  url_list

    def getImg(self, html):
        parseHtml = etree.HTML(html)
        r_list = parseHtml.xpath('//img[@class="BDE_Image"]/@src')
        return r_list

    def imgPage(self, u_list):
        img_list = []
        for url in u_list:
            res = requests.get(url, headers=self.headers)
            res.encoding = "utf-8"
            img_l = self.getImg(res.text)
            img_list.append(img_l)
        return img_list

    def writeImg(self, img_list):
        lt = []
        for url_list in img_list:
            sleep(0.1)
            self.writerFile(url_list)

    def writerFile(self, img_list):
        if os.path.exists('static/img') is not True:
            os.mkdir('static/img')
        for url in img_list:
            res = requests.get(url, headers=self.headers)
            data = res.content
            with open("static/img/%s.jpg" % url[-12:-4], "wb") as f:
                f.write(data)
            self.l.append("static/img/%s.jpg" % url[-12:-4])

    def workOn(self, kw, p=None):
        # kw = input("请输入贴吧名称：")
        img_list = []
        while True:
            html = self.getPage(kw, self.url)
            url_list = self.parsePage(html)
            img_list += url_list
            # c = input("第%d页已经贴吧已经下载完毕，是否继续(y/n):"%self.page)
            p = int(p)
            if p > self.page:
                print("第%d页获取资源中，请稍侯..."%self.page)
                self.page += 1
                self.pn = (self.page - 1)*50
            else:
                print("获取资源中，请稍侯...")
                break
        i_list = self.imgPage(img_list)
        self.writeImg(i_list)
        return self.l


if __name__ == "__main__":
    kw = input("请输入贴吧名称：")
    spider = TiebaSpider()
    imglist = spider.workOn(kw)