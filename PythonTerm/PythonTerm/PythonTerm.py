# -*- coding: utf-8 -*-
import sys
import urllib.request
import string
import base64
import codecs
from xml.dom.minidom import *

loop = True
api_key = "pXzMF6%2Fw76xCHSzsvA1g%2BW5SFbBIk2dWoUF91PDp%2FN3UvF84Wq0io0KPhbT9VyE9Z7o9YgiUGqsMrCTfp55Fvw%3D%3D"

def addParsingDicList(xmlData, motherData, childData):
    # ?Ľ̵? ?????͸? ????Ʈ?? ?־ ???? ?Ѵ?.
    doc = parseString(xmlData)
    siGunGuList = doc.getElementsByTagName(motherData)
    signguCdSize = len(siGunGuList)
    list = []
    for index in range(signguCdSize):
        mphms = siGunGuList[index].getElementsByTagName(childData)
        if  ( mphms.length != 0):
            list.append(str(mphms[0].firstChild.data))
        else:
            list.append(str("No Data"))
    return list

def openAPItoXML(server, key, value):
    #?ѱ? ?ּ?
    req = urllib.request.Request(server + key + value)
    req.add_header = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    data = urllib.request.urlopen(req).read().decode('utf-8')
    return data

def localSearch():
    server2 = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaCode?ServiceKey="
    value2 = "&MobileOS=ETC&MobileApp=AppTesting&numOfRows=1000"
    
    
    
    realdata = openAPItoXML(server2, api_key, value2)
    
    localList = addParsingDicList(realdata, "item", "name")
    localListNum = addParsingDicList(realdata, "item", "code")
    
    print(localList)
    #print(localListNum)
    
    local = input("지역을 적어주세요 : ")
    
    for i in localList:
        if ( local == i ):
            local = localListNum[localList.index(i)]
    
    #print(local)
    server2 = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchFestival?ServiceKey="
    value2 = str("&areaCode=") + str(local) + str("&MobileOS=ETC&MobileApp=AppTesting&contentTypeId=15")
    
    #print(value2)
    
    realdata = openAPItoXML(server2, api_key, value2)
    
    #print(realdata)
    eventLocal = addParsingDicList(realdata, "item", "addr1")
    eventName = addParsingDicList(realdata, "item", "title")
    eventTel = addParsingDicList(realdata, "item", "tel")
    eventStartDate = addParsingDicList(realdata, "item", "eventstartdate")
    eventEndDate = addParsingDicList(realdata, "item", "eventenddate")
    eventImage = addParsingDicList(realdata, "item", "firstimage")
    
    for i in eventLocal:
            print(str("\nName : ") + eventName[eventLocal.index(i)] + str("\nLocal : ") + i + str("\nTel : ") + eventTel[eventLocal.index(i)] +  str("\nStarDate : ") + eventStartDate[eventLocal.index(i)] + str("\nEndDate : ") + eventEndDate[eventLocal.index(i)] + str  ("\nImage : ") + eventImage[eventLocal.index(i)] + str("\n") )
    

def keywordSearch():
    server2 = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchKeyword?ServiceKey="
    keyword = input("키워드를 적어주세요 : ")
    keyword = urllib.parse.quote(keyword)
    value2 = "&keyword=" + str(keyword) + "&MobileOS=ETC&MobileApp=AppTesting&contentTypeId=15"
    
    realdata = openAPItoXML(server2, api_key, value2)
    
    #print(realdata)
    eventLocal = addParsingDicList(realdata, "item", "addr1")
    eventName = addParsingDicList(realdata, "item", "title")
    eventTel = addParsingDicList(realdata, "item", "tel")
    eventImage = addParsingDicList(realdata, "item", "firstimage")

    for i in eventLocal:
            print(str("\nName : ") + eventName[eventLocal.index(i)] + str("\nLocal : ") + i + str("\nTel : ") + eventTel[eventLocal.index(i)] + str  ("\nImage : ") + eventImage[eventLocal.index(i)] + str("\n") )
    


while (loop == True):
    print("------------------------------------------------------------------")
    print("1. 지역검색")
    print("2. 텍스트 검색")
    print("3. 종료")
    print("------------------------------------------------------------------")
    key_num = input("번호를 입력해주세요 : ")

    if int(key_num) == 1:
        localSearch()
    

    if int(key_num) == 2:
       keywordSearch()

    if int(key_num) == 3:
        loop = False;
    

