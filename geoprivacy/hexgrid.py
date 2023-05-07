import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)   
from h3 import h3
import folium
import json

def assemble_polylines(hexagons):
    polylines = []
    lat = []
    lng = []
    for hex_ in hexagons:
        polygons = h3.h3_set_to_multi_polygon([hex_], geo_json=False)
        # flatten polygons into loops.
        outlines = [loop for polygon in polygons for loop in polygon]
        polyline = [outline + [outline[0]] for outline in outlines][0]
        # append versus extend (url reference below):
        #     https://stackoverflow.com/questions/252703/
        #        what-is-the-difference-between-pythons-list-methods-append-and-extend
        lat.extend(map(lambda v:v[0],polyline)) # gets all lats
        lng.extend(map(lambda v:v[1],polyline)) # gets all lons
        polylines.append(polyline) # gets all hexagons

    return polylines    
    
def visualize_hexagons(hexagons, color="red", folium_map=None, zoom_start=13):
    """
    hexagons is a list of hexcluster. Each hexcluster is a list of hexagons. 
    eg. [[hex1, hex2], [hex3, hex4]]
    """
    polylines = []
    lat = []
    lng = []
    for hex_ in hexagons:
        polygons = h3.h3_set_to_multi_polygon([hex_], geo_json=False)
        # flatten polygons into loops.
        outlines = [loop for polygon in polygons for loop in polygon]
        polyline = [outline + [outline[0]] for outline in outlines][0]
        # append versus extend (url reference below):
        #     https://stackoverflow.com/questions/252703/
        #        what-is-the-difference-between-pythons-list-methods-append-and-extend
        lat.extend(map(lambda v:v[0],polyline)) # gets all lats
        lng.extend(map(lambda v:v[1],polyline)) # gets all lons
        polylines.append(polyline) # gets all hexagons
    
    if folium_map is None:
        # default map
        m = folium.Map(location=[sum(lat)/len(lat), sum(lng)/len(lng)], zoom_start=zoom_start, tiles='cartodbpositron')
    else:
        # custom map
        m = folium_map
    # iterate through hexagons, add each to map
    for polyline in polylines:
        my_PolyLine=folium.PolyLine(locations=polyline,\
                                    weight=1,opacity=0.8, color=color)
        m.add_child(my_PolyLine)
    return m
    
def visualize_polygon(polyline, color):
    polyline.append(polyline[0])
    lat = [p[0] for p in polyline]
    lng = [p[1] for p in polyline]
    m = folium.Map(location=[sum(lat)/len(lat), sum(lng)/len(lng)], zoom_start=13, tiles='cartodbpositron')
    my_PolyLine=folium.PolyLine(locations=polyline,weight=8,color=color)
    m.add_child(my_PolyLine)
    return m

def get_h3_neighbors(h3_address, layers=1):
    neighbors = h3.k_ring_distances(h3_address, layers)
    return neighbors

def get_h3_address(latlon, resolution):
    lat, lon = latlon
    h3_address = h3.geo_to_h3(lat, lon, resolution)
    return h3_address

def read_json(file):
    with open(file) as f:
      json_file = json.load(f)
    return json_file
