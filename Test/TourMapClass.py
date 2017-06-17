import folium
import webbrowser

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