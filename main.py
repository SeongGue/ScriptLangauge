import folium
import http.client
import webbrowser
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

class TourMap:
    html_name = "tour_map.html"
    def __init__(self):
        self.tour_map = folium.Map (location = [37, 127], zoom_start=7)

    def AddMarker(self, title, mapX, mapY):
        folium.Marker([mapY, mapX], popup=title).add_to(self.tour_map)

    def saveMapData(self):
        self.tour_map.save(self.html_name)

    def openHTML(self):
        webbrowser.open(self.html_name)


def main():
    APIServer = TourAPI()
    tour_map = TourMap()
    date = input()
    festival_list = APIServer.GetFastivalData(date)
    for d in festival_list:
        tour_map.AddMarker(d["FastivalTitle"], d["mapX"], d["mapY"])
    tour_map.saveMapData()
    tour_map.openHTML()

main()

