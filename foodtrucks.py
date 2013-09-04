#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import Flask, abort, jsonify, render_template, request, url_for
from math import radians, cos, sin, asin, sqrt
from pygeocoder import Geocoder
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/foodtrucks', methods = ["GET"])
def foodtrucks():
    address = request.args.get('location')
    if address:
        user_location = geocode_location(address)
    else:
        lat, lng = request.args.get('lat'), request.args.get('lng')
        user_location = (float(lat), float(lng))
    if not user_location:
        abort(404)
    bounds = calculate_bounds(user_location)
    trucks = get_foodtrucks(location=user_location, bounds=bounds)
    unique_trucks = remove_duplicates(trucks, user_location)
    location = {"lat": user_location[0], "lng": user_location[1]}
    return json.dumps({'coordinates': location, 'foodtrucks': unique_trucks})

def geocode_location(address):
    """ Returns the lat, lng coordinates of the given address or False if the address is invalid
    """
    try:
        result = Geocoder.geocode(address)
        lat, lng = result[0].coordinates
        if result.city != "San Francisco":  # Database only returns foodtrucks in San Francisco
            return None
        return lat, lng
    except:
        return None

def calculate_bounds(user_location, r=1):
    """ Returns a dictionary of the northwestern & southeastern coordinates that bound the location by a specified radius
    """
    try:
        lat, lng = user_location
    except: 
        return None
    MILES_IN_DEGREE = 69.0
    distance_lat = r/MILES_IN_DEGREE # North-south distance 
    distance_lng = distance_lat/cos(lat) # East-west distance 
    nw, se = (lat+distance_lat,lng-distance_lng), (lat-distance_lat,lng+distance_lng)
    return nw, se

def get_foodtrucks(location, bounds):
    """ Returns the list of trucks recieved from the database
    """
    northwest, southeast = bounds
    nw_lat, nw_lng = northwest
    se_lat, se_lng = southeast
    PARAM_TEMPLATE = "$where=within_box(location, {:f}, {:f}, {:f}, {:f})"
    params = PARAM_TEMPLATE.format(nw_lat, nw_lng, se_lat, se_lng)
    r = requests.get('http://data.sfgov.org/resource/rqzj-sfat.json', params=params)
    return r.json()

def remove_duplicates(trucks, user_location):
    """ Returns a list of unique truck entries
    """
    unique_foodtrucks = {}
    for truck in trucks:
        key = truck['applicant']
        if key in unique_foodtrucks:
            existing_truck = float(truck['latitude']), float(truck['longitude'])
            current_truck = float(unique_foodtrucks[key]['latitude']), float(unique_foodtrucks[key]['longitude'])
            if distance(user_location, existing_truck) < distance(user_location, current_truck):
                unique_foodtrucks[key] = truck
        else:
            unique_foodtrucks[key] = truck
    return unique_foodtrucks.values()

def distance(loc1, loc2):
    """ Calculates the distance between two points
    """
    x1, y1 = loc1
    x2, y2 = loc2
    return sqrt((y2-y1)**2 + (x2-x1)**2)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)