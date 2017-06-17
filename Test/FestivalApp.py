from TkUIClass import*
from xml.dom.minidom import *

tour_map = TourMap()
APIServer = TourAPI()

imageURLList = []
mailData = []

#오늘 날짜로 행사 정보 검색
date = datetime.datetime.now()
dateForm = date.strftime("%Y%m%d")
festival_list = APIServer.GetFastivalData(dateForm)

def SetMapData():
    for d in festival_list:
        tour_map.AddMarker(d["FastivalTitle"], d["mapX"], d["mapY"])
    tour_map.saveMapData()


def OpenMap():
    tour_map.openHTML()


def SendMail():
    global InputLabel

    host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
    port = "587"
    html = ""
    title = InputLabel.get() + " 검색 결과"
    senderAddr = "scg1221@gmail.com"
    recipientAddr = "game_son20@naver.com"
    msgtext = "메일 테스트"
    passwd = "Naice@73027242"
    msgtext = 'y'
    if msgtext == 'y':
        # keyword = str(input('input keyword to search:'))
        for text in mailData:
            html += text
            html += "<br>"

    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    # set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset='UTF-8')

    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    msg.attach(bookPart)

    print("connect smtp server ... ")
    s = mysmtplib.MySMTP(host, port)
    # s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)  # 로긴을 합니다.
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()

    print("Mail sending complete!!!")


def SearchButtonAction():
    global SearchListBox
    SearchIndex = SearchListBox.curselection()[0]

    if SearchIndex == 0:
        LocalSearch()
    elif SearchIndex == 1:
        keywordSearch()

def ShowImageButton():
    ResultListIndex = ResultListBox.curselection()[0]
    imageIndex = int(ResultListIndex / 5)
    Festival_APP.InitURLImage(330, 220, 30, 350, imageURLList[imageIndex])

def LocalSearch():
    global InputLabel
    global ResultListBox
    global imageURLList
    global scrollbar
    global mailData

    fontData = font.Font(Festival_APP.window, size=13, weight='bold', family='Consolas')
    ResultListBox = Festival_APP.InitListBox(39, 5, 0, 210, fontData, scrollbar.set)
    imageURLList = []

    local = 0
    # RenderText.insert(INSERT, InputLabel.get())
    server2 = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaCode?ServiceKey="
    value2 = "&MobileOS=ETC&MobileApp=AppTesting&numOfRows=1000"
    api_key = "pXzMF6%2Fw76xCHSzsvA1g%2BW5SFbBIk2dWoUF91PDp%2FN3UvF84Wq0io0KPhbT9VyE9Z7o9YgiUGqsMrCTfp55Fvw%3D%3D"

    realdata = openAPItoXML(server2, api_key, value2)

    localList = addParsingDicList(realdata, "item", "name")
    localListNum = addParsingDicList(realdata, "item", "code")

    for i in localList:
        if (InputLabel.get() == i):
            local = localListNum[localList.index(i)]

    server2 = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchFestival?ServiceKey="
    value2 = str("&areaCode=") + str(local) + str("&MobileOS=ETC&MobileApp=AppTesting&contentTypeId=15")

    realdata = openAPItoXML(server2, api_key, value2)

    # print(realdata)
    eventLocal = addParsingDicList(realdata, "item", "addr1")
    eventName = addParsingDicList(realdata, "item", "title")
    eventTel = addParsingDicList(realdata, "item", "tel")
    eventStartDate = addParsingDicList(realdata, "item", "eventstartdate")
    eventEndDate = addParsingDicList(realdata, "item", "eventenddate")
    eventImage = addParsingDicList(realdata, "item", "firstimage")

    listboxIndex = 0
    for i in eventLocal:
        ResultListBox.insert(listboxIndex, "이름 : " + eventName[eventLocal.index(i)])
        mailData.append("이름 : " + eventName[eventLocal.index(i)])
        listboxIndex += 1
        ResultListBox.insert(listboxIndex, "주소 : " + i)
        mailData.append("주소 : " + i)
        listboxIndex += 1
        ResultListBox.insert(listboxIndex, "전화번호 : " + eventTel[eventLocal.index(i)])
        mailData.append("전화번호 : " + eventTel[eventLocal.index(i)])
        listboxIndex += 1
        ResultListBox.insert(listboxIndex, "시작일 : " + eventStartDate[eventLocal.index(i)])
        mailData.append("시작일 : " + eventStartDate[eventLocal.index(i)])
        listboxIndex += 1
        ResultListBox.insert(listboxIndex, "종료일 : " + eventEndDate[eventLocal.index(i)])
        mailData.append("종료일 : " + eventEndDate[eventLocal.index(i)])
        listboxIndex += 1
        imageURLList.append(eventImage[eventLocal.index(i)])

def keywordSearch():
    print("키워드검색")

def openAPItoXML(server, key, value):
    req = urllib.request.Request(server + key + value)
    req.add_header = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    data = urllib.request.urlopen(req).read().decode('utf-8')
    return data

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

SetMapData()

Festival_APP = TkUI()

fontData = font.Font(Festival_APP.window, size=15, weight="bold", family="Consolas")
Festival_APP.InitLabel("[나 들 이 : 전국 행사 정보 서비스]", 25, 0, fontData)

fontData = font.Font(Festival_APP.window, size=12, weight="bold", family="Consolas")
Festival_APP.InitLabel("<지역 검색>", 80, 35, fontData)

fontData = font.Font(Festival_APP.window, size=9, weight="bold", family="Consolas")
Festival_APP.InitLabel("서울,인천,대전,대구,광주,부산,울산,세종특별자치시,", 80, 55, fontData)

fontData = font.Font(Festival_APP.window, size=9, weight="bold", family="Consolas")
Festival_APP.InitLabel("경기도,강원도,충청북도,충청남도,경상북도,경상남도,", 80, 70, fontData)

fontData = font.Font(Festival_APP.window, size=9, weight="bold", family="Consolas")
Festival_APP.InitLabel("전라북도,전라남도,제주도", 80, 85, fontData)

Festival_APP.Initimage("나들이.gif", 0, 35)

fontData = font.Font(Festival_APP.window, size=13, weight='bold', family='Consolas')
SearchListBox = Festival_APP.InitListBox(10, 1, 0, 110, fontData, Festival_APP.InitScrollbar(115, 110).set)
SearchListBox.insert(1, "지역 검색")
SearchListBox.insert(2, "텍스트 검색")

fontData = font.Font(Festival_APP.window, size=12, weight='bold', family='Consolas')
Festival_APP.InitButton("G메일 보내기", SendMail, 140, 115, fontData)

fontData = font.Font(Festival_APP.window, size=12, weight='bold', family='Consolas')
Festival_APP.InitButton("행사 위치 보기", OpenMap, 255, 115, fontData)

fontData = font.Font(Festival_APP.window, size=13, weight='bold', family='Consolas')
InputLabel = Festival_APP.InitEntry(26, 0, 0, 160, fontData)

fontData = font.Font(Festival_APP.window, size=13, weight='bold', family='Consolas')
Festival_APP.InitButton("검색", SearchButtonAction, 265, 162, fontData)

fontData = font.Font(Festival_APP.window, size=13, weight='bold', family='Consolas')
Festival_APP.InitButton("이미지", ShowImageButton, 317, 162, fontData)

fontData = font.Font(Festival_APP.window, size=13, weight='bold', family='Consolas')
scrollbar = Festival_APP.InitScrollbar(370, 250)
ResultListBox = Festival_APP.InitListBox(39, 5, 0, 210, fontData, scrollbar.set)
scrollbar.pack(side=RIGHT, fill=BOTH)

fontData = font.Font(Festival_APP.window, size=9, weight="bold", family="Consolas")
Festival_APP.InitLabel("공공데이터포털 : 국문관광서비스", 200, 575, fontData)

Festival_APP.window.mainloop()

