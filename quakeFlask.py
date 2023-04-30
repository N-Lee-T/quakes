from flask import Flask, render_template, url_for, request, redirect 
import requests
import json
import sys
 
app = Flask(__name__)

# if we need to look up lat / lon from a location, fill in this function
# currently just has dummy values
# try: https://radar.com/content/alternatives/google-maps-api-vs-radar
#
# def get_lat_lon():
    # """
    # Gets the latitude and longitude for a given location, or the location if already given
    # TO DO: implement getting coordinates for a given location

    # ::param:: to be determined

    # ::returns:: Latitude and longitude values in a 2-item list []
    # """
    # lat_lon = [43, -91]
    # return lat_lon

def get_quakes(coords, period): 
    """
    Gets data about earthquakes in the specificied time period from USGS, then determines nearest quake

    ::param coords:: A 2-item list of [latitude, longitude]
    ::param period:: string - represention of time period for which quakes are to be fetched (can be 'h', 'd', or 'm')

    ::returns::  JSON object containing three values: 'count' of total quakes
                                                      'magnitude' of nearest quake
                                                      'location' of nearest quake
    """
    if period == 'h':
        # within the last hour
        url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson'
        time = 'last hour'
    elif period == 'd':
        # all quakes within the last day
        url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'
        time = 'last 24 hours'
    else:
        # all quakes within the last month - this takes a while...
        url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson'
        time = 'last month'

    # w/o taking params
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson'
    time = 'hour'

    # fetch the info from USGS API using the end point specified
    usgs_req = requests.get(url)

    # get JSON representation of data, and the features (quakes)
    usgs_info = usgs_req.json()
    recent_quakes = usgs_info['features']

    # determine the closest quake and the number recorded in the time frame
    count, minQuake = 0, sys.maxsize
    closest = None
    for quake in recent_quakes:
        # print(quake["geometry"]["coordinates"], quake["geometry"]["coordinates"][0], type(quake["geometry"]["coordinates"][0]), int(quake["geometry"]["coordinates"][0]), type(int(quake["geometry"]["coordinates"][0])))
        print(coords, coords[0], type(coords[0]))
        lat = int(coords[0]) - int(quake["geometry"]["coordinates"][0]) 
        lon = int(coords[1]) - int(quake["geometry"]["coordinates"][1]) 
        tot = abs(lat + lon) 
        if tot < minQuake:
            minQuake = tot
            closest = quake
        count += 1
    quake_facts = {
        "count": count,
        "location": closest['properties']['title'][8:],
        "magnitude": closest['properties']['mag']
    }

    # if returning JSON object, use this
    return(quake_facts)

    # else, if rendering page, use this
    # return recent_quakes, count, closest, time

@app.route("/", methods=["GET", "POST"])
def start():
    """
    Simply renders the starting page
    """
    return render_template('index.html')

@app.route("/quakes", methods=["GET"])
def get_those_quakes():
    """
    Calls methods to get coordinates and interact with USGS API
    Example of URL string: 'http://localhost:5000/quakes?time=h&lat=43&lon=%2D91' - note %2D url encoding for ' - '
                           'http://localhost:5000/quakes?time=h&lat=43&lon=65' - no URL encoding for negative value

    ::returns:: JSON object if calling externally
                Flask template if calling internally
    """
    period = request.args.get('time')

    # coords = get_lat_lon()
    coords = [None, None]
    coords[0], coords[1] = request.args.get('lat'), request.args.get('lon')

    # send the data if using in other application
    quake = get_quakes(coords, period)
    return(json.dumps(quake))

    # show the data if rendering webpage
    # recent_quakes, count, closest, time = get_quakes(coords, period)
    # return render_template('quakes.html', recent_quakes=recent_quakes, count=count, closest=closest, time=time)

if __name__=='__main__':
    app.run(debug=True)

## remember to check for negative latitudes and include %2D in URL string when implementing form!!