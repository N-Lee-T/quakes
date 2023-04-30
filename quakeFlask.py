from flask import Flask, render_template, url_for, request, redirect 
import requests
import json
import sys
 
app = Flask(__name__)

def get_lat_lon():
    lat_lon = [43, -91]
    return lat_lon

def get_quakes(coords, period): 

    # if period == 'h':
    #     # within the last hour
    #     url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson'
    #     time = 'last hour'
    # elif period == 'd':
    #     # all quakes within the last day
    #     url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'
    #     time = 'last 24 hours'
    # else:
    #     # all quakes within the last month - this takes a while...
    #     url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson'
    #     time = 'last month'

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
        lat = coords[0] - int(quake["geometry"]["coordinates"][0]) 
        lon = coords[1] - int(quake["geometry"]["coordinates"][1]) 
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
    # return(quake_facts)

    # else, if rendering page, use this
    return recent_quakes, count, closest, time

@app.route("/", methods=["GET", "POST"])
def yes():
    return render_template('index.html')

@app.route("/quakes", methods=["GET"])
def hellyes():
    period = request.args.get['time']
    # coords[0], coords[1] = request.args.get['lat'], request.args.get['lon']
    # may need to add functionality to get coordinates
    coords = get_lat_lon()

    # send the data if using in other application
    # quake = get_quakes
    # return(json.dumps(quake))

    # show the data if rendering webpage
    recent_quakes, count, closest, time = get_quakes(coords, period)
    return render_template('quakes.html', recent_quakes=recent_quakes, count=count, closest=closest, time=time)

if __name__=='__main__':
    app.run(debug=True)

