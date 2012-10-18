yahooGeoPlanet
==============

A library to get information of the Yahoo! GeoPlanet™
This little library provides methods which you can use to read information of the Yahoo! GeoPlanet API.
I have tried to respect the structure of the JSON so the methods simply parse Json Objects to Python Objects.
If you want more about the structure of the JSON returned by yahoo api check: http://developer.yahoo.com/geo/geoplanet/guide/api_docs.html

There are four classes:
- yahooGeoPlanet: It is the main class and therefore contains the main methods. Must to be always instantiate.
	methods: 
			- def getPlaceByWoeid(self,woeid) : Returns a place object specified by WOEID.
			- def getWoeidByPlace(self,query): Returns a list of place object specified which match with the query.
			- def getRangeOfWoeid(self,query,count): Returns a list of place objects of length equals the value of count. Ordered by the most likely.
 			- def getParentWoeid(self,woeid): Returns a place object which contains the parent of a given WOEID.
 			- getLang/setLang : A getter/setter to get/set the language of the requests. English default

- Place: It is a simple deserialization of the place object given by the api to a Python object. This object provides a collection of getters/setters to get WOEID,Country, administration...
- Attributes: Generally contains information of the administration.
- Coordinates: An object which contains latitude and longitude.
- yahooGeoError: If something went wrong, main methods return a yahooGeoError object with information of the error.