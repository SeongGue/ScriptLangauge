# -*- coding: utf-8 -*-
import sys
import urllib.request
import string
import base64
import codecs
from xml.dom.minidom import *
from tkinter import *
from tkinter import font
import tkinter.messagebox
g_Tk = Tk()
g_Tk.title("나들이")
g_Tk.geometry("400x600+750+200")
DataList = []
api_key = "pXzMF6%2Fw76xCHSzsvA1g%2BW5SFbBIk2dWoUF91PDp%2FN3UvF84Wq0io0KPhbT9VyE9Z7o9YgiUGqsMrCTfp55Fvw%3D%3D"

def addParsingDicList(xmlData, motherData, childData):
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
    req = urllib.request.Request(server + key + value)
    req.add_header = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    data = urllib.request.urlopen(req).read().decode('utf-8')
    return data

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="<전국 행사정보 서비스>")
    MainText.pack()
    MainText.place(x=80)

def InitTopText2():
    TempFont = font.Font(g_Tk, size=7, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="<지역 검색>'서울,인천,대전,대구,광주,부산,울산,세종특별자치시,경기도,")
    MainText.pack()
    MainText.place(x=80, y=35)

def InitTopText3():
    TempFont = font.Font(g_Tk, size=7, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="강원도,충청북도,충청남도,경상북도,경상남도,전라북도,전라남도,제주도'")
    MainText.pack()
    MainText.place(x=80, y=50)

def mainimage():
    img = PhotoImage(file='나들이.gif')
    lbl = Label(image=img)
    lbl.image = img  # 레퍼런스 추가
    lbl.place(x=0, y=0)

def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=150, y=80)
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',width=10, height=1, borderwidth=12, relief='ridge',yscrollcommand=ListBoxScrollbar.set)
    SearchListBox.insert(1, "지역 검색")
    SearchListBox.insert(2, "텍스트 검색")
    SearchListBox.pack()
    SearchListBox.place(x=10, y=80)

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=130)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=138)

def SearchButtonAction():
    global SearchListBox

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)  
    iSearchIndex = SearchListBox.curselection()[0]
    if iSearchIndex == 0:
        Search()
    elif iSearchIndex == 1:
        pass

    RenderText.configure(state='disabled')

def Search():
    server2 = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaCode?ServiceKey="
    value2 = "&MobileOS=ETC&MobileApp=AppTesting&numOfRows=1000"

    realdata = openAPItoXML(server2, api_key, value2)
    
    localList = addParsingDicList(realdata, "item", "name")
    localListNum = addParsingDicList(realdata, "item", "code")
    
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
                RenderText.insert(INSERT, "[")
                RenderText.insert(INSERT, i + 1)
                RenderText.insert(INSERT, "] ")
                RenderText.insert(INSERT, "시설명: ")
                RenderText.insert(INSERT, eventName)
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "주소: ")
                RenderText.insert(INSERT, eventLocal)
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "전화번호: ")
                RenderText.insert(INSERT, eventTel)
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "시작일: ")
                RenderText.insert(INSERT, eventStartDate)
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "종료일: ")
                RenderText.insert(INSERT, eventEndDate)
                RenderText.insert(INSERT, "\n\n")
    

def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=185)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

InitTopText()
InitRenderText()
InitSearchButton()
InitInputLabel()
InitTopText()
mainimage()
InitSearchListBox()
InitTopText3()
InitTopText2()
g_Tk.mainloop()