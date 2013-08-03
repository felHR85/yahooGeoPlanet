yahooGeoPlanet
==============
NOW IT WORKS WITH PYTHON 3

A wrapper to get information of the Yahoo! GeoPlanet™
This little wrapper provides methods which you can use to read information of the Yahoo! GeoPlanet API.
I have tried to respect the structure of the JSON so the methods simply parse Json Objects to Python Objects.
If you want more about the structure of the JSON returned by yahoo api check: http://developer.yahoo.com/geo/geoplanet/guide/api_docs.html

There are four classes:
- GeoPlanet: It is the main class and therefore contains the main methods. Must to be always instantiate.
	methods: 
			<blockquote> def get_place_by_woeid(self,woeid)</blockquote>  Returns a list of place object specified by WOEID. Usually with one object
			<blockquote> def get_woeid_by_place(self,query)</blockquote>  Returns a list of place object specified which match with the query.
			<blockquote> def get_range_of_woeid(self,query,count)</blockquote>  Returns a list of place objects of length equals the value of count. Ordered by the most likely.
 			<blockquote> def get_parent_woeid(self,woeid)</blockquote>  Returns a place object which contains the parent of a given WOEID.

- Place: It is a simple deserialization of the place object given by the api to a Python object. 
- Attributes: Generally contains information of the administration.
- Coordinates: An object which contains latitude and longitude.
- GeoError: If something went wrong, main methods return a yahooGeoError object with information of the error.
