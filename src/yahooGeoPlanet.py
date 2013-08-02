"""
Copyright (c) 2012 Felipe Herranz

Permission is hereby granted, free of charge, to any
person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the
Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice
shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import http.client as httplib
import urllib
import json

class GeoPlanet(object):
	""" Main class. A yahoo Id is needed"""

	def __init__(self,yahooId):

		self.__yahooId = str(yahooId)
		self.__uri = 'where.yahooapis.com'
		self.__connection = httplib.HTTPConnection(self.__uri)
		self.lang = "en"

	def get_place_by_woeid(self,woeid):

		""" Returns a place object specified by WOEID. """
		params = "/v1/place/" + str(woeid) + "?lang=" + self.__lang +"&format=json&appid=" + self.__yahooId
		self.__connection.request("GET",params)
		httpResponse = self.__connection.getresponse()

		try:
			if httpResponse.status != 200:
				errorCode = httpResponse.status
				typeError = "Http Connection failed: " + str(errorCode)
				raise yahooGeoError(typeError)
		except yahooGeoError as error:
			return error

		data = httpResponse.read()
		data = json.loads(data)
		placeJson = data["place"]
		placeObject = Place.parse_place(placeJson)
		return placeObject


	def get_woeid_by_place(self,query):

		""" Returns a list of place object specified which match with the query. """

		query = urllib.parse.quote(query)
		params = "/v1/places.q('" + query +"')" + "?lang=" + self.__lang +"&format=json&appid=" + self.__yahooId
		self.__connection.request("GET",params)
		httpResponse = self.__connection.getresponse()

		try:
			if httpResponse.status != 200:
				errorCode = httpResponse.status
				typeError = "Http Connection failed: " + str(errorCode)
				raise yahooGeoError(typeError)
		except yahooGeoError as error:
			return error 

		data = httpResponse.read()
		data = json.loads(data)

		try:  # If there is not a single place object in the Json (you can know it checking "total parameter") raise an exception
			if data["places"].get("total") == 0:
				messageError = "This query has not results"
				raise yahooGeoError(messageError)
		except yahooGeoError as error:
			return error

		placeJson = data["places"].get("place")
		placeList = list()

		for itemPlace in placeJson:

			placeList.append(Place.parse_place(placeJson)) 

		return placeList

	def get_range_of_woeid(self,query,count):

		""" Returns a list of place objects of length equals the value of count. Ordered by the most likely. """
		query = urllib.parse.quote(query)
		params = "/v1/places.q('" + query + "');start=0;count=" + str(count) + "?lang=" + self.__lang +"&format=json&appid=" + self.__yahooId
		self.__connection.request("GET",params)
		httpResponse = self.__connection.getresponse()

		try:
			if httpResponse.status != 200:
				errorCode = httpResponse.status
				typeError = "Http Connection failed: " + str(errorCode)
				raise yahooGeoError(typeError)
		except yahooGeoError as error:
			return error 

		data = httpResponse.read()
		data = json.loads(data)
		

		try:# If there is not a single place object in the Json (you can know it checking "total parameter") raise an exception
			if data["places"].get("total") == 0:
				messageError = "This query has not results"
				raise yahooGeoError(messageError)
		except yahooGeoError as error:
			return error

		placeJson = data["places"].get("place")
		placeList = list()

		
		for itemPlace in placeJson:

			placeList.append(Place.parse_place(placeJson)) 

		return placeList

	def get_parent_woeid(self,woeid):

		""" Returns a place object which contains the parent of a given WOEID. """

		params = "/v1/place/" + str(woeid) + "/parent?lang=" +  self.__lang + "&format=json&select=long&appid=" + self.__yahooId
		self.__connection.request("GET",params)
		httpResponse = self.__connection.getresponse()

		try:
			if httpResponse.status != 200:
				errorCode = httpResponse.status
				typeError = "Http Connection failed: " + str(errorCode)
				raise yahooGeoError(typeError)
		except yahooGeoError as error:
			return error 

		data = httpResponse.read()
		data = json.loads(data)
		placeJson = data["place"]
		placeObject = Place.parse_place(placeJson)
		return placeObject

	# def getNeighborsWoeid(self,woeid):

	# 	params = "/v1/place/" + str(woeid) + "/neighbors?lang=" + str(self.__lang) +  "&format=json&appid=" + str(self.__yahooId)
	# 	params = {"params":params}
	# 	encodedParams = urllib.urlencode(params)
	# 	self.__connection.request("GET",encodedParams["params"])
	# 	httpResponse = self.__connection.getresponse()

	# 	try:
	# 		if httpResponse.status != 200:
	# 			errorCode = httpResponse.status
	# 			typeError = "Http Connection failed: " + str(errorCode)
	# 			raise yahooGeoError(typeError)
	# 	except yahooGeoError, error:
	# 		return error 

	# 	data = httpResponse.read()
	# 	data = json.loads(data)

	
class Place(object):

	""" A representation of the information given by the JSON. It is practically the same information of the JSON """

	@classmethod
	def parse_place(cls,placeJson):
		place = cls()
		place.woeid = placeJson["woeid"]
		place.placeTypeName = placeJson["placeTypeName"]
		place.placeTypeName_attr = Attributes(None,placeJson["placeTypeName attrs"].get("code"))
		place.name = placeJson["name"]
		place.country = placeJson["country"]
		place.country_attrs = Attributes(placeJson["country attrs"].get("type"),placeJson["country attrs"].get("code"))
		place.admin1 = placeJson["admin1"]
		place.admin1_attrs = Attributes(placeJson["admin1 attrs"].get("type"),placeJson["admin1 attrs"].get("code"))
		place.admin2 = placeJson["admin2"]
		place.admin2_attrs = Attributes(placeJson["admin2 attrs"].get("type"),placeJson["admin2 attrs"].get("code"))
		place.admin3 = placeJson["admin3"]
		place.locality1 = placeJson["locality1"]
		place.locality1_attrs = Attributes(placeJson["locality1 attrs"].get("type"),None)
		place.locality2 = placeJson["locality2"]
		place.postal = placeJson["postal"]
		place.centroid = Coordinates("centroid",placeJson["centroid"].get("latitude"),placeJson["centroid"].get("longitude"))

		southwestCoord = Coordinates("southWest",placeJson["boundingBox"].get("southWest").get("latitude"),placeJson["boundingBox"].get("southWest").get("longitude"))
		northEastCoord = Coordinates("northEast",placeJson["boundingBox"].get("northEast").get("latitude"),placeJson["boundingBox"].get("northEast").get("longitude"))

		place.boundingBox = list().append(southwestCoord)
		place.boundingBox.append(northEastCoord)
		place.uri = placeJson["uri"]
		place.lang = placeJson["lang"]
		return place



class Attributes(object):

	""" In the yahooGeoPlanet model of data, administrations, countries and localities have some attributes like type and code. This class contains them """

	def __init__(self,Type,code):

		self.type = Type
		self.code = code


class Coordinates(object):

	""" A class which contains latitude and longitude """

	def __init__(self,name,latitude,longitude):

		self.name = name
		self.latitude = latitude
		self.longitude = longitude


class GeoError(Exception):

	"""  If something went wrong, main methods return a yahooGeoError object with information of the error. """

	def __init__(self,typeError):

		self.typeError = typeError

"""
Unicode functions
"""
str_to_utf8 = lambda s: s.encode('utf-8')
utf8_to_str = lambda s: str(s,'utf-8')







