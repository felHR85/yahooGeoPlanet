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

import httplib
import urllib
import json

class yahooGeoPlanet(object):
	""" Main class. A yahoo Id is needed"""

	def __init__(self,yahooId):

		self.__yahooId = yahooId
		self.__uri = 'where.yahooapis.com'
		self.__connection = httplib.HTTPConnection(self.__uri)
		self.__lang = "en"

	def getPlaceByWoeid(self,woeid):

		""" Returns a place object specified by WOEID. """

		params = "/v1/place/" + str(woeid) + "?lang=" + str(self.__lang) +"&format=json&appid=" + str(self.__yahooId)
		self.__connection.request("GET",params)
		httpResponse = self.__connection.getresponse()

		try:
			if httpResponse.status != 200:
				errorCode = httpResponse.status
				typeError = "Http Connection failed: " + str(errorCode)
				raise yahooGeoError(typeError)
		except yahooGeoError, error:
			return error

		data = httpResponse.read()
		data = json.loads(data)
		placeJson = data["place"]
		placeObject = self.__readJson(placeJson)
		return placeObject


	def getWoeidByPlace(self,query):

		""" Returns a list of place object specified which match with the query. """

		query = unicode(query).encode('utf-8')
		query = urllib.quote(query)
		params = "/v1/places.q('" + str(query) +"')" + "?lang=" + str(self.__lang) +"&format=json&appid=" + str(self.__yahooId)
		self.__connection.request("GET",params)
		httpResponse = self.__connection.getresponse()

		try:
			if httpResponse.status != 200:
				errorCode = httpResponse.status
				typeError = "Http Connection failed: " + str(errorCode)
				raise yahooGeoError(typeError)
		except yahooGeoError, error:
			return error 

		data = httpResponse.read()
		data = json.loads(data)

		try:  # If there is not a single place object in the Json (you can know it checking "total parameter") raise an exception
			if data["places"].get("total") == 0:
				messageError = "This query has not results"
				raise yahooGeoError(messageError)
		except yahooGeoError, error:
			return error

		placeJson = data["places"].get("place")
		placeList = list()

		for itemPlace in placeJson:

			placeList.append(self.__readJson(itemPlace)) 

		return placeList

	def getRangeOfWoeid(self,query,count):

		""" Returns a list of place objects of length equals the value of count. Ordered by the most likely. """

		query = unicode(query).encode('utf-8')
		query = urllib.quote(query)
		params = "/v1/places.q('" + str(query) + "');start=0;count=" + str(count) + "?lang=" + str(self.__lang) +"&format=json&appid=" + str(self.__yahooId)
		self.__connection.request("GET",params)
		httpResponse = self.__connection.getresponse()

		try:
			if httpResponse.status != 200:
				errorCode = httpResponse.status
				typeError = "Http Connection failed: " + str(errorCode)
				raise yahooGeoError(typeError)
		except yahooGeoError, error:
			return error 

		data = httpResponse.read()
		data = json.loads(data)
		

		try:# If there is not a single place object in the Json (you can know it checking "total parameter") raise an exception
			if data["places"].get("total") == 0:
				messageError = "This query has not results"
				raise yahooGeoError(messageError)
		except yahooGeoError, error:
			return error

		placeJson = data["places"].get("place")
		placeList = list()

		
		for itemPlace in placeJson:

			placeList.append(self.__readJson(itemPlace)) 

		return placeList

	def getParentWoeid(self,woeid):

		""" Returns a place object which contains the parent of a given WOEID. """


		params = "/v1/place/" + str(woeid) + "/parent?lang=" +  str(self.__lang) + "&format=json&select=long&appid=" + str(self.__yahooId)
		self.__connection.request("GET",params)
		httpResponse = self.__connection.getresponse()

		try:
			if httpResponse.status != 200:
				errorCode = httpResponse.status
				typeError = "Http Connection failed: " + str(errorCode)
				raise yahooGeoError(typeError)
		except yahooGeoError, error:
			return error 

		data = httpResponse.read()
		data = json.loads(data)
		placeJson = data["place"]
		placeObject = self.__readJson(placeJson)
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

	def setLang(self,lang):

		self.__lang = lang

	def getLang(self):

		return self.__lang




	def __readJson(self,placeJson): # A private method with all json operations

		placeObject = place()
		placeObject.setWoeid(placeJson["woeid"])
		placeObject.setPlaceTypeName(placeJson["placeTypeName"])
		attr = attributes(None,placeJson["placeTypeName attrs"].get("code"))
		placeObject.setPlaceTypeNameAttrs(attr)
		placeObject.setName(placeJson["name"])
		placeObject.setCountry(placeJson["country"])
		attrCountry = attributes(placeJson["country attrs"].get("type"),placeJson["country attrs"].get("code"))
		placeObject.setCountryAttrs(attrCountry)
		placeObject.setAdmin1(placeJson["admin1"])
		attrAdmin1 = attributes(placeJson["admin1 attrs"].get("type"),placeJson["admin1 attrs"].get("code"))
		placeObject.setAdmin1Attrs(attrAdmin1)
		placeObject.setAdmin2(placeJson["admin2"])
		attrAdmin2 = attributes(placeJson["admin2 attrs"].get("type"),placeJson["admin2 attrs"].get("code"))
		placeObject.setAdmin2Attrs(attrAdmin2)
		placeObject.setAdmin3(placeJson["admin3"])
		placeObject.setLocality1(placeJson["locality1"])
		attrLocality1 = attributes(placeJson["locality1 attrs"].get("type"),None)
		placeObject.setLocality1Attrs(attrLocality1)
		placeObject.setLocality2(placeJson["locality2"])
		placeObject.setPostal(placeJson["postal"])
		centroidCoord = coordinates("centroid",placeJson["centroid"].get("latitude"),placeJson["centroid"].get("longitude"))
		placeObject.setCentroid(centroidCoord)
		southwestCoord = coordinates("southWest",placeJson["boundingBox"].get("southWest").get("latitude"),placeJson["boundingBox"].get("southWest").get("longitude"))
		northEastCoord = coordinates("northEast",placeJson["boundingBox"].get("northEast").get("latitude"),placeJson["boundingBox"].get("northEast").get("longitude"))
		listBoundingBox = list()
		listBoundingBox.append(southwestCoord)
		listBoundingBox.append(northEastCoord)
		placeObject.setBoundingBox(listBoundingBox)
		placeObject.setUri(placeJson["uri"])
		placeObject.setLang(placeJson["lang"])

		return placeObject



class place(object):

	""" A representation of the information given by the JSON. It is practically the same information of the JSON """
	""" There are a lot of getters/setters for each value you may neeed. An example of JSON object is included in folder test """

	def __init__(self):

		self.__woeid = None
		self.__placeTypeName = None
		self.__placeTypeName_attrs = None
		self.__name = None
		self.__country = None
		self.__country_attrs = None
		self.__admin1 = None
		self.__admin1_attrs = None
		self.__admin2 = None
		self.__admin2_attrs = None
		self.__admin3 = None
		self.__locality1 = None
		self.__locality1_attrs = None
		self.__locality2 = None
		self.__postal = None
		self.__centroid = None
		self.__boundingBox = list()
		self.__uri = None
		self.__lang = None

	

	def setWoeid(self,woeid):

		self.__woeid = woeid

	def getWoeid(self):

		return self.__woeid

	def setPlaceTypeName(self,placeTypeName):

		self.__placeTypeName = placeTypeName

	def getPlaceTypeName(self):
	
		return self.__placeTypeName 

	def setPlaceTypeNameAttrs(self,placeTypeNameAttrs):

		self.__placeTypeName_attrs = placeTypeNameAttrs

	def getPlaceTypeNameAttrs(self):

		return self.__placeTypeName_attrs

	def setName(self,name):

		self.__name = name

	def getName(self):

		return self.__name

	def setCountry(self,country):

		self.__country = country

	def getCountry(self):

		return self.__country

	def setCountryAttrs(self,countryAttrs):

		self.__country_attrs = countryAttrs

	def getCountryAttrs(self):

		return self.__country_attrs

	def setAdmin1(self,admin1):

		self.__admin1 = admin1

	def getAdmin1(self):

		return self.__admin1

	def setAdmin1Attrs(self,admin1Attrs):

		self.__admin1_attrs = admin1Attrs

	def getAdmin1Attrs(self):

		return self.__admin1_attrs

	def setAdmin2(self,admin2):

		self.__admin2 = admin2

	def getAdmin2(self):

		return self.__admin2

	def setAdmin2Attrs(self,admin2Attrs):

		self.__admin2_attrs = admin2Attrs

	def getAdmin2Attrs(self):

		return self.__admin2_attrs

	def setAdmin3(self,admin3):

		self.__admin3 = admin3

	def getAdmin3(self):

		return self.__admin3

	def setLocality1(self,locality1):

		self.__locality1 = locality1

	def getLocality1(self):

		return self.__locality1

	def setLocality1Attrs(self,locality1Attrs):

		self.__locality1_attrs = locality1Attrs

	def getLocality1Attrs(self):

		return self.__locality1_attrs

	def setLocality2(self,locality2):

		self.__locality2 = locality2

	def getLocality2(self):

		return self.__locality2

	def setPostal(self,postal):

		self.__postal = postal

	def getPostal(self):

		return self.__postal

	def setCentroid(self,centroid):

		self.__centroid = centroid

	def getCentroid(self):

		return self.__centroid

	def setBoundingBox(self,boundingBox):

		self.__boundingBox = boundingBox

	def getBoundingBox(self):

		return self.__boundingBox

	def setUri(self,uri):

		self.__uri = uri

	def getUri(self):

		return self.__uri

	def setLang(self,lang):

		self.__lang = lang

	def getLang(self):

		return self.__lang

class attributes(object):

	""" In the yahooGeoPlanet model of data, administrations, countries and localities have some attributes like type and code. This class contain them """

	def __init__(self,Type,code):

		self.__type = Type
		self.__code = code

	def getType(self):

		return self.__type

	def getCode(self):

		return self.__code

class coordinates(object):

	""" A class which contains latitude and longitude """

	def __init__(self,name,latitude,longitude):

		self.__name = name
		self.__latitude = latitude
		self.__longitude = longitude

	def getName(self):

		return self.__name

	def getLatitude(self):

		return self.__latitude

	def getLongitude(self):

		return self.__longitude

class yahooGeoError(Exception):

	"""  If something went wrong, main methods return a yahooGeoError object with information of the error. """

	def __init__(self,typeError):

		self.__typeError = typeError

	def getTypeError(self):

		return self.__typeError











