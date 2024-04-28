import folium

# Create a map centered at a specific location
mymap = folium.Map(location=[0, 0], zoom_start=2)

# Add markers for the coordinates
marker1 = folium.Marker(location=[40.7128, -74.0060], popup="Marker 1", icon=folium.Icon(color='blue'))
marker2 = folium.Marker(location=[34.0522, -118.2437], popup="Marker 2", icon=folium.Icon(color='red'))

# Add markers to the map
marker1.add_to(mymap)
marker2.add_to(mymap)

# Save the map to an HTML file
mymap.save("map.html")