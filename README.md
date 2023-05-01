# Quakes 
This microservice application uses real-time USGS JSON feeds to return data about the nearest earthquake to a given location within a time period specified by the user.

## Requesting data from this microservice

Data can be retrieved by making a GET request to a base url with three parameters. The data for the parameters can be obtained in any way that the client wishes, but the url must contain all three or it will not return any data. 

+ LOCATION - Currently, the program requires both latitude and longitude coordinates. This could be changed in an update to require only a place name.
  + LATITUDE (lat): The latitudinal position of the location
  + LONGITUDE (lon): The longitudinal position of the location
  
  **lat** and **lon** MUST be in integer or float format. That means that ticks ( ' ), degree symbol, or more than one period are not acceptable input.

  Acceptable: 
  - 43.56800
  - 43.568
  - 43.56
  - 43.5
  - 43
  - -43

  Not acceptable: 
  - 43°34'04.8"N 
  - 43°34'04.8" 
  - 43°34'04.8" 
  - 43°34'04.8" 
  - 43S
  - -43° 
  - 43 S

+ TIME PERIOD (time): The period of time (hour, last 24 hours, or month) for which we are looking for nearby earthquakes 
Times: 
  - 'h' or 'H' for last hour
  - 'd' or 'D' for last 24 hours
  - 'm' or 'M' for last month

The url can be constructed in the request as shown below (Python, but other languages would be similar):
`result = requests.get(url=url, time=time, lat=lat, lon=lon).json()`
Notice that time, lat, and lon must be specified as the parameters in the request

Or it can be constructed using string methods (again, in Python):
`url = 'http://localhost:5000/quakes?time={}&lat={}&lon={}'.format(period, latitude, longitude)`

In any case, the successful call to the endpoint will need to be implemented with a url that looks like the following: 
`http://localhost:5000/quakes?time=h&lat=43&lon=&2D91`

In this example, the URL is requesting earthquakes within the last hour ('time=h') and we will be looking for the quake nearest to latitude 43N ('lat=43') and longitude 91 West / -91 ('lon=&2D91). 

**Note that west longitudes (negative, like '-91') and south latitudes (negative, like -21) must be URL-encoded. This means prefacing with '&2D', so that '-91' becomes '&2D91'. **

## Receiving data from this microservice
This service will provide a JSON object to the client containing three pieces of data: 
Count of the total number of earthquakes recorded by USGS during the specified period (hour, last 24 hours, month)
Location of the nearest earthquake during the specified period (string description, with varying levels of detail)
Magnitude of the nearest earthquake

This JSON object can be parsed using any method that the client wishes to implement. A simple example:
`print(f"\nOf the {result['count']} quakes, the nearest quake was (in) {result['location']}, and its magnitude was {result['magnitude']}\n")`


# Sequence Diagram

![Sequence diagram of the quakes microservice](https://user-images.githubusercontent.com/98563878/235463877-8352f260-df0c-4063-aed2-c70195aa4100.png)

