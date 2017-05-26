import folium

map_osm = folium.Map (location = [37.568477, 126.981611],
zoom_start=13)
folium.Marker([37.568477, 126.981611], popup='Mt. Hood Meadows').add_to(map_osm)
map_osm.save('osm.html')