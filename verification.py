# -*- coding: utf-8 -*-
import http.cookiejar
import urllib.request
from os import close, write
import re
import os
from bs4 import BeautifulSoup
from pathlib import Path 

list_path = Path('./verification/list_letou63')
path = os.getcwd()
with open(list_path, 'r', encoding='utf-8') as testlist:
    for full_line in testlist.readlines():
        testlink = 'http://' + \
            re.search('(?<=\t)\w+.\w+.\w+', full_line).group()
        # 抓出長域名中邀請碼的部分
        invite_code = re.search('(?<=/a/|/t/)[0-9]+', full_line).group()
        # urllib.request.urlopen(testlink).geturl() 重新導向取得跳轉後的網址
        # re.search('\S*(?<=/cn/|/vn/|/th/)', full_line).group()從list的長域名抓到CN,VN,TH為止
        if urllib.request.urlopen(testlink).geturl() == re.search('\S*(?<=/cn/|/vn/|/th/)', full_line).group():
            # 宣告一個CookieJar物件例項來儲存cookie
            cookie = http.cookiejar.CookieJar()
            # 利用urllib2庫的HTTPCookieProcessor物件來建立cookie處理器
            handler = urllib.request.HTTPCookieProcessor(cookie)
            # 通過handler來構建opener
            opener = urllib.request.build_opener(handler)
            # 此處的open方法同urllib2的urlopen方法，也可以傳入request
            response = opener.open(testlink)
            for item in cookie:
                if item.name == "ksdi3":
                    if item.value == invite_code:
                        print(testlink + '設置成功')
        else:
            print(testlink + '短域名DNS解析有誤')
