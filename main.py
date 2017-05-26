import folium

map_osm = folium.Map (location = [37.568477, 126.981611],
zoom_start=13)
folium.Marker([37.568477, 126.981611], popup='Mt. Hood Meadows').add_to(map_osm)
map_osm.save('osm.html')

import http.client
conn = http.client.HTTPConnection("api.visitkorea.or.kr")
conn.request("GET", "/openapi/service/rest/KorService/locationBasedList?ServiceKey=oW569yK18Ye1fnoHw6siNC8d5gmugwkVC6urxBJB3cOBSgFxcWnpm3tDCm3UeVZ4PR4rGDEuYIM4pKuSUXyEYg%3D%3D&contentTypeId=39&mapX=126.981611&mapY=37.568477&radius=500&pageNo=1&numOfRows=10&listYN=Y&arrange=A&MobileOS=ETC&MobileApp=AppTesting", ) #서버에 GET 요청
req = conn.getresponse() #openAPI 서버에서 보내온 요청을 받아옴
print(req.status,req.reason)
#cLen = req.getheader("Content-Length") #가져온 데이터 길이
strXml = req.read() #데이터 읽기

from xml.etree import ElementTree

tree = ElementTree.fromstring(strXml)
print (strXml)
# Book 엘리먼트를 가져옵니다.
itemElements = tree.getiterator("item")  	# item 엘리먼트 리스트 추출
print(itemElements)
for item in itemElements:
    addr = item.find("addr1")    		#isbn 검색
    strTitle = item.find("title") 		#title 검색
    print(addr.text)
    print (strTitle.text)
