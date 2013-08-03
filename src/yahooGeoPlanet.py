"""
Copyright (c) 2013 Felipe Herranz

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

	def __init__(self, yahooId):

		self._yahooId = str(yahooId)
		self.lang = "en"

	def get_place_by_woeid(self, woeid):

		call = Binder.binder(params="/v1/place/", lang="?lang=" + self.lang, yahooId="&format=json&appid=" + self._yahooId)
		return call(woeid=str(woeid))
	
	def get_woeid_by_place(self, query):

		""" Returns a list of place object specified which match with the query. """
		call = Binder.binder(params_query="/v1/places.q('", lang="?lang=" + self.lang, yahooId="&format=json&appid=" + self._yahooId)
		return call(query=query)
		

	def get_range_of_woeid(self, query, count):

		""" Returns a list of place objects of length equals the value of count. Ordered by the most likely. """
		call = Binder.binder(params_query="/v1/places.q('", lang="?lang=" + self.lang, yahooId="&format=json&appid=" + self._yahooId)
		return call(query=query, count=str(count))

	def get_parent_woeid(self, woeid):

		""" Returns a place object which contains the parent of a given WOEID. """
		call = Binder.binder(params="/v1/place/", lang="?lang=" + self.lang, yahooId="&format=json&appid=" + self._yahooId)
		return call(woeid=str(woeid))

	
class Place(object):

	""" A representation of the information given by the JSON. It is practically the same information of the JSON """

	@classmethod
	def parse_place(cls, placeJson):
		place = cls()
		place.woeid = placeJson["woeid"]
		place.placeTypeName = placeJson["placeTypeName"]
		place.placeTypeName_attr = Attributes(None, placeJson["placeTypeName attrs"].get("code"))
		place.name = placeJson["name"]
		place.country = placeJson["country"]
		place.country_attrs = Attributes(placeJson["country attrs"].get("type"),placeJson["country attrs"].get("code"))
		place.admin1 = placeJson["admin1"]
		place.admin1_attrs = Attributes(placeJson["admin1 attrs"].get("type"),placeJson["admin1 attrs"].get("code"))
		place.admin2 = placeJson["admin2"]
		place.admin2_attrs = Attributes(placeJson["admin2 attrs"].get("type"),placeJson["admin2 attrs"].get("code"))
		place.admin3 = placeJson["admin3"]
		place.locality1 = placeJson["locality1"]
		place.locality1_attrs = Attributes(placeJson["locality1 attrs"].get("type"), None)
		place.locality2 = placeJson["locality2"]
		place.postal = placeJson["postal"]
		place.centroid = Coordinates("centroid",placeJson["centroid"].get("latitude"),placeJson["centroid"].get("longitude"))

		southwestCoord = Coordinates("southWest", placeJson["boundingBox"].get("southWest").get("latitude"), placeJson["boundingBox"].get("southWest").get("longitude"))
		northEastCoord = Coordinates("northEast", placeJson["boundingBox"].get("northEast").get("latitude"), placeJson["boundingBox"].get("northEast").get("longitude"))

		place.boundingBox = list()
		place.boundingBox.append(southwestCoord)
		place.boundingBox.append(northEastCoord)
		place.uri = placeJson["uri"]
		place.lang = placeJson["lang"]
		return place



class Attributes(object):

	""" In the yahooGeoPlanet model of data, administrations, countries and localities have some attributes like type and code. This class contains them """

	def __init__(self, Type, code):

		self.type = Type
		self.code = code


class Coordinates(object):

	""" A class which contains latitude and longitude """

	def __init__(self, name, latitude, longitude):

		self.name = name
		self.latitude = latitude
		self.longitude = longitude


class GeoError(Exception):

	"""  If something went wrong, main methods return a yahooGeoError object with information of the error. """

	def __init__(self, typeError):

		self.typeError = typeError


class Binder(object):

	_uri = 'where.yahooapis.com'

	@classmethod
	def binder(cls,**url_config):

		def _geo_call(**kwargs):
			# Set url parameters
			params = url_config.get("params", None)
			params_query = url_config.get("params_query", None)
			lang = url_config.get("lang")
			yahooId = url_config.get("yahooId")
			start = url_config.get("start", None)

			woeid = kwargs.get("woeid", None)
			query = kwargs.get("query", None)
			count = kwargs.get("count", None)

			if params is not None:
				params_str = params + woeid + lang + yahooId
			elif params_query is not None and start is None:
				params_str = params_query + urllib.parse.quote(query) + "')" + lang + yahooId
			else:
				params_str = params_query + urllib.parse.quote(query) + "');start=0;count=" + count + lang + yahooId
			
			# Http connection
			conn = httplib.HTTPConnection(cls._uri)
			conn.request("GET", params_str)
			http_response = conn.getresponse()

			if http_response.status != 200:
				error_code = http_response.status
				type_error = "Http Connection failed: " + str(error_code)
				raise GeoError(type_error)

			# Parsing
			list_place = list()
			data = str(http_response.read(),'utf-8')

			data = json.loads(data)
			if data.get("place", None) is not None:
				list_place.append(Place.parse_place(data["place"]))
			else:
				places_json = data["places"]
				places = places_json["place"]
				for item in places:
					list_place.append(Place.parse_place(item))
			return list_place

		return _geo_call








