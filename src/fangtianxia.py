# -*- coding:utf-8 -*-
import re

import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
# import sys

host = "http://zu.fang.com"
def getNextPageUrl(bs:BeautifulSoup,nextPageCount:int):
    nextPage = bs.find(class_="fanye").find_all("a", text=nextPageCount)
    if nextPage is not None:
        return host+nextPage[0].get("href")
    else:
        return None

def getPage(url):
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "lxml")
    return bs

def getHouseDetail(house:BeautifulSoup):
    priceDiv = house.select_one("[calss~=trl-item sty1]")
    # priceDiv = house.find("div",class_="trl-item sty1")
    print(priceDiv)
    price = priceDiv.i.string;
    p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配
    p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配
    bedroomStr = house.find_all(class_="tt")[0].text.replace("（","(").replace("）",")")
    bedroom = re.findall(r"(.*?)[(]",bedroomStr)[0]
    rentalType = re.findall(p1,bedroomStr)[0]
    bedroomType = house.find_all(class_="tt")[1].text.replace("（","(").replace("）",")")
    size = house.find_all(class_="tt")[2].text.replace("（","(").replace("）",")")
    turnTowards = house.find_all(class_="tt")[3].text.replace("（","(").replace("）",")")
    floor = house.find_all(class_="tt")[4].text.replace("（","(").replace("）",")")
    decoration = house.find_all(class_="tt")[5].text.replace("（","(").replace("）",")")
    brokerName = house.find(class_="zf_jjname").a.string
    brokerMobile = house.find(class_="text_phone").string
    intermediary = house.find(class_="tjcont-list-cline2 tjcont_gs clearfix").span.string
    attr = {}
    attr["bedroom"] = bedroom
    attr["rentalType"] = rentalType
    attr["bedroomType"] = bedroomType
    attr["size"] = size
    attr["turnTowards"] = turnTowards
    attr["floor"] = floor
    attr["decoration"] = decoration
    attr["brokerName"] = brokerName
    attr["brokerMobile"] = brokerMobile
    attr["intermediary"] = intermediary

    fyms = {}
    fyldLi = house.find(class_="fyld")
    if fyldLi is not None:
        fyld = fyldLi.find(class_="fyms_title").string
        fyldValList = fyldLi.find(class_="fyms_con").stripped_strings
        fyldVal = "\n".join(fyldValList)
        fyms[fyld] = fyldVal
    hxjsLi = house.find(class_="hxjs")
    if hxjsLi is not None:
        hxjs = hxjsLi.find(class_="fyms_title").string
        hxjsValList = hxjsLi.find(class_="fyms_con").stripped_strings
        hxjsVal = "\n".join(hxjsValList)
        fyms[hxjs] = hxjsVal
    xqjsLi = house.find(class_="xqjs")
    if xqjsLi is not None:
        xqjs = xqjsLi.find(class_="fyms_title").string
        xqjsValList = xqjsLi.find(class_="fyms_con").stripped_strings
        xqjsVal = "\n".join(xqjsValList)
        fyms[xqjs] = xqjsVal
    zbptLi = house.find(class_="zbpt")
    if zbptLi is not None:
        zbpt = zbptLi.find(class_="fyms_title").string
        zbptValList = zbptLi.find(class_="fyms_con").stripped_strings
        zbptVal = "\n".join(zbptValList)
        fyms[zbpt] = zbptVal
    jtcxLi = house.find(class_="jtcx")
    if jtcxLi is not None:
        jtcx = jtcxLi.find(class_="fyms_title").string
        jtcxValList = jtcxLi.find(class_="fyms_con").stripped_strings
        jtcxVal = "\n".join(jtcxValList)
        fyms[jtcx] = jtcxVal
    attr["fyms"]=fyms

    ptss = house.find(class_="content-item zf_new_ptss")
    ptssVal = ""
    if ptss is not None:
        ptss = ptss.find(class_="cont clearfix").ul
        for p in ptss:
            ptssVal = ptssVal+p.string
    attr["ptss"] = ptssVal

    fytp = house.find(class_="cont-sty1")
    fytpList = []
    if fytp is not None:
        fytp = fytp.findAll("img")
        for f in fytp:
            fytpList.append("http:"+f["src"])
    attr["fytp"] = fytpList
    return attr

def getBs(url):
    pass

def getHouseUrlList(bs:BeautifulSoup):
    houseList = bs.find_all("dd", attrs={"class": "info rel"});
    houseUrlList = [];
    for house in houseList:
        houseUrlList.append(host +house.p.a.get("href"))
    return houseUrlList

def getFangZi(dd:BeautifulSoup):

    title = dd.a.get("title")
    url = host+dd.a.get("href")
    attr = dd.find(class_="font15 mt12 bold").text
    woshi = attr.split("|")[0].strip()
    hezu = attr.split("|")[1]
    daxiao = attr.split("|")[2].strip()[:-2]
    chaoxiang = attr.split("|")[3]

    quyu = dd.find(class_="gray6 mt12").text
    note = dd.select(".mt12 .note")
    notes = []
    for n in note:
        notes.append(n.getText())
    price = dd.find(class_="price").text +"元/月"
    # sys.setdefaultencoding("utf-8")
    with open("a.txt","a",encoding='utf-8') as f:
        f.write(newLine(title))
        f.write(newLine(woshi+"|"+hezu+"|"+daxiao+"|"+chaoxiang))
        f.write(newLine(quyu))
        f.write(newLine("|".join(notes)))
        f.write(newLine(price))
        f.write(newLine("===================================================================================="))

def newLine(data):
    return data.strip() + "\n"

def getPageUrl(bs,pageCount):
    # print(bs)
    currentPage = bs.find(class_="fanye").find_all("a",text=pageCount)
    # nextPage = bs.find(calss_="fanye",text=pageCount);
    return host+currentPage[0].get("href")


if __name__ == '__main__':
    currentPageCount = 1
    pageUrl = host+"/house1/zhu-j011-k0236/n33/"
    # while (1==1):
    #     bs = getPage(pageUrl)
    #     houseUrlList = getHouseUrlList(bs)
    #     for houseUrl in houseUrlList:
    #         print(houseUrl)
    #         house = getPage(houseUrl)
    #         attr = getHouseDetail(house)
    #         print(attr)
    #     pageUrl = getNextPageUrl(bs,currentPageCount+1)
    #     if pageUrl is None:
    #         break

    house = getPage("http://zu.fang.com/chuzu/1_61159229_-1.htm")
    attr = getHouseDetail(house)
    print(attr)





    # while (1==1):
    #     url = getPageUrl(bs,currentPageCount)
    #     bs = getBs(url)
    #     print(dds)
    #     for dd in dds:
    #         getFangZi(dd)



    # fanye = bs.find(class_="fanye").find_all("a")
    # url = [];
    # for f in fanye:
    #     url.append(host+f.get("href"))
    # for index,f in enumerate(url):
    #     if index == 0 or index > len(fanye)-3:
    #         continue
    #     page1 = getPage(f);
    #     content = getContent(page1)
    #     for dd in content:
    #         getFangZi(dd)