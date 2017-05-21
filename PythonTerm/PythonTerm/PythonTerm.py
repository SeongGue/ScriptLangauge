# -*- coding: utf-8 -*-
import sys
import urllib.request
import string
import base64
import codecs
from xml.dom.minidom import *

def addParsingDicList(xmlData, motherData, childData):
    # 파싱된 데이터를 리스트에 넣어서 리턴 한다.
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
    #한글 주석
    req = urllib.request.Request(server + key + value)
    req.add_header = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    data = urllib.request.urlopen(req).read().decode('utf-8')
    return data


server2 = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaCode?ServiceKey="
key2 = "pXzMF6%2Fw76xCHSzsvA1g%2BW5SFbBIk2dWoUF91PDp%2FN3UvF84Wq0io0KPhbT9VyE9Z7o9YgiUGqsMrCTfp55Fvw%3D%3D"
value2 = "&MobileOS=ETC&MobileApp=AppTesting&numOfRows=1000"



realdata = openAPItoXML(server2, key2, value2)

localList = addParsingDicList(realdata, "item", "name")
localListNum = addParsingDicList(realdata, "item", "code")

print(localList)
print(localListNum)

print("Local List : ")
local = input()

for i in localList:
    if ( local == i ):
        local = localListNum[localList.index(i)]

print(local)
server2 = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey="
value2 = str("&areaCode=") + str(local) + str("&MobileOS=ETC&MobileApp=AppTesting&contentTypeId=15")

#print(value2)

realdata = openAPItoXML(server2, key2, value2)


#print(realdata)
eventLocal = addParsingDicList(realdata, "item", "addr1")
eventName = addParsingDicList(realdata, "item", "title")
eventImage = addParsingDicList(realdata, "item", "firstimage")


for i in eventLocal:
        print(str("Local : ") + i + str("\nName : ") + eventName[eventLocal.index(i)] + str("\nImage : ") + eventImage[eventLocal.index(i)] )

