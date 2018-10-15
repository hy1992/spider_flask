#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: huang time:20180424
from flask import Flask
from flask import render_template
from flask import request
import qrcode
import time
from requests.exceptions import ChunkedEncodingError
from qiubai import QbSpider
from tie import TiebaSpider
import json
# 实例化对象为app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('url.html')

@app.route('/qb',methods=['GET','POST'])
def qiubai():
    if request.method == 'GET':
        return  render_template('qiubai.html')
    # tname = request.form.get('tname')
    page = request.form.get('page')
    try:
        spi = QbSpider()
        q_list = spi.workOn(p=page)
        # user = json.dumps(q_list)
    except ChunkedEncodingError as e:
        print("线程异常,忽略...")
    except Exception as ee:
        print(ee)
    finally:
        return render_template('show_qiubai.html',user=q_list)

@app.route('/tb',methods=['GET','POST'])
def tieba():
    if request.method == 'GET':
        return  render_template('tb.html')
    tname = request.form.get('tname')
    page = request.form.get('page')
    try:
        spi = TiebaSpider()
        img_list = spi.workOn(kw=tname,p=page)
        img_list = list(set(img_list))
    except ChunkedEncodingError as e:
        print("线程异常,忽略...")
    except Exception as ee:
        print(ee)
    finally:
        return render_template('show_img.html', img_l=img_list)


@app.route('/url',methods=['GET','POST'])
def url():
    if request.method == 'GET':
        return u'当前为GET请求'
    http_url = request.form.get('text')  # post请求
    img = qrcode.make(http_url)
    path = 'static/qrimg/%s.png' % time.time()
    img.save(path)
    return render_template('img.html', qrimg=path)

@app.route('/1.png')
def png():
    return open('1.png', 'rb').read()

@app.route('/text',methods=['GET','POST'])
def text():
    if request.method == 'GET':
        return render_template('text.html')
    text = request.form.get('text').encode('utf-8')
    if len(text) <= 1108:
        img = qrcode.make(text)
        path = 'static/qrimg/%s.png' % time.time()
        img.save(path)
        return render_template('img.html', qrimg=path)
    fn_path = 'static/%s.txt' % time.time()
    with open(fn_path, 'w') as fn:
        fn.write(text)
    path = 'static/qrimg/%s.png' % time.time()
    img = qrcode.make('http://127.0.0.1:5000/%s' % fn_path)
    img.save(path)
    return render_template('img.html', qrimg=path)

if __name__ == '__main__':
    app.run(debug=True)