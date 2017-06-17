import http.client
from xml.etree import ElementTree

class TourAPI:
    def __init__(self):
        self.ServerAddr = "api.visitkorea.or.kr"
        self.BasicRequest = "/openapi/service/rest/KorService/searchFestival"
        self.ServiceKey = "?ServiceKey=oW569yK18Ye1fnoHw6siNC8d5gmugwkVC6urxBJB3cOBSgFxcWnpm3tDCm3UeVZ4PR4rGDEuYIM4pKuSUXyEYg%3D%3D"
        self.OSAndAppName = "&MobileOS = ETC & MobileApp = Nadry"
        self.conn = http.client.HTTPConnection(self.ServerAddr)

    def GetFastivalData(self, startDate):
        self.conn.request("GET", self.BasicRequest + self.ServiceKey + "&eventStartDate=" + startDate + "&arrange=A&listYN=Y&pageNo=1&numOfRows=10" + self.OSAndAppName)
        req = self.conn.getresponse()
        print(req.status, req.reason)
        strXml = req.read()  # 데이터 읽기

        # 원하는 데이터 추출
        tree = ElementTree.fromstring(strXml)
        print(strXml)
        # Book 엘리먼트를 가져옵니다.
        itemElements = tree.getiterator("item")  # item 엘리먼트 리스트 추출
        print(itemElements)
        FastivalList = []
        for item in itemElements:
            mapX = item.find("mapx")  # isbn 검색
            mapY = item.find("mapy")
            strTitle = item.find("title")  # title 검색
            FastivalData = {"FastivalTitle" : strTitle.text, "mapX" : eval(mapX.text), "mapY" : eval(mapY.text)}
            FastivalList.append(FastivalData)

        return FastivalList