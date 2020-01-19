#!/usr/bin/python
# -*- Coding: utf-8 -*-

from selenium import webdriver
import time
import urllib.request  #クローラのライブラリ
import urllib.robotparser   #robots.txtを読むためのパッケージ
from bs4 import BeautifulSoup  #スクレイピングのライブラリ
import sys
import datetime
import csv

yobi = ["月","火","水","木","金","土","日"]
year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day
weekday = yobi[datetime.date.today().weekday()]

f = open(str(datetime.date.today()) + '.csv','w',encoding='utf_8_sig')
write_sentence = ['年', '月', '日', '曜日', '台', '台番号', 'BIG', 'REG', '合成確率', '累計ゲーム']      #記事名、URL、内容という列を作成
writer = csv.writer(f, lineterminator='\n')
writer.writerow(write_sentence)


mobile_emulation = { "deviceName": "Nexus 5" }
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome("C:/chromedriver.exe", desired_capabilities = chrome_options.to_capabilities())
driver.get("URL")
time.sleep(3)


# スロット一覧ページを全件表示
while(1):
    if "ulKIm" in driver.page_source:
        try:
            time.sleep(3)
            driver.find_element_by_id("ulKIm").click()
        except:
            break
source_html = driver.page_source

# HTMLを解析、台のURLを取得
soup = BeautifulSoup(source_html)
soup_select = soup.select_one("#ulKI")
soup_a = soup_select.find_all("a")

url_base = "https://www.pscube.jp/dedamajyoho-P-townDMMpachi/c709203/cgi-bin/"
slot_dic = {}

for line in soup_a:
    slot_dic[line.find("div").string] = url_base + line.get("href")

# それぞれの台に遷移して、台番号をすべて取得
url2 = "https://www.pscube.jp"

for slot in slot_dic:
    driver.get(slot_dic[slot])
    dai_dic = {}
    time.sleep(5)
    html2 = driver.page_source
    soup2 = BeautifulSoup(html2)
    soup_select = soup2.select_one("#tblDAb")
    soup_a = soup_select.find_all("a")
    for line in soup_a:
        dai_dic[line.find("div").string] = url2 + line.get("href")

    for dai in dai_dic:
        driver.get(dai_dic[dai])
        time.sleep(5)
        html3 = driver.page_source
        soup3 = BeautifulSoup(html3)
        soup_select = soup3.select_one("#tblDAb")
        for line in soup_select:
            try:
                tmp = line.find("td").string
                for i, hoge in enumerate(line):
                    if i == 3:
                        temp = hoge.string
                if tmp == "BIG":
                    big = temp
                elif tmp == "REG":
                    reg = temp
                elif tmp == "合成確率":
                    gousei = temp
                elif tmp == "累計ゲーム":
                    ruikei = temp

            except:
                pass

        write_sentence = [year, month, day, weekday, slot, dai, big, reg, gousei, ruikei]
        writer.writerow(write_sentence)    #CSVに追記
f.close()
