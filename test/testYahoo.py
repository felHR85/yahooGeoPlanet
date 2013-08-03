#-*- coding: utf-8 -*-
import yahooGeoPlanet

yahooId = "Your Yahoo Id here"

geoPlanet = yahooGeoPlanet.GeoPlanet(yahooId) # Instantiate a yahooGeoPlanet object
geoPlanet.lang= "en" # set language to english
madrid = geoPlanet.get_woeid_by_place('Madrid')
barcelona = geoPlanet.get_woeid_by_place("Barcelona")  # get two place objects with data of Madrid and Barcelona

# if isinstance(madrid,yahooGeoError):
# 	print madrid.getTypeError if we get an error
# else:

""" Get some information of each object: Woeid code, country of the place, kind of administration, uri of the data and the latitude of Madrid."""
woeidM = madrid[0].woeid
countryM = madrid[0].country
uriM = madrid[0].uri
admin1M = madrid[0].admin1
latitudM = madrid[0].centroid.latitude

woeidB = barcelona[0].woeid
countryB = barcelona[0].country
uriB = barcelona[0].uri
admin1B = barcelona[0].admin1
admin1AttrB = barcelona[0].admin1_attrs.type



""" Print Data """

print ("Woeid of Madrid: " + str(woeidM) + " Country of Madrid : " + countryM + " Uri: " + uriM + " admin1: " + admin1M + " latitude: " + str(latitudM))
print (" ")
print (" ")
print ("Woeid of Barcelona: " + str(woeidB) + " Country of Barcelona: " + countryB + " Uri: " + uriB + " admin1: " + admin1B + " admin1 attributes: " + admin1AttrB)
print (" ")
print (" ")


""" Now We check if we have a valid Woeid we can get information """
newPlace = geoPlanet.get_place_by_woeid(2397733)
# print newPlace.getTypeError() if we get an error

city = newPlace[0].name
woeidB = newPlace[0].woeid
countryB = newPlace[0].country
uriB = newPlace[0].uri
admin1B = newPlace[0].admin1
admin1AttrB = newPlace[0].admin1_attrs.type
print ("Woeid 2397733: " + city + " WOEID code: " + str(woeidB) + " Country: " + countryB + " Uri: " + uriB + " admin1: " + admin1B + " admin1 atributos: " + admin1AttrB)
print (" ")
print (" ")

""" We need to know the parent Woeid code of a given woeid which we know it is from Amarillo. Where is Amarillo? """
amarilloTexas = geoPlanet.get_parent_woeid(12792500)

parent = amarilloTexas[0].admin1
# print amarilloTexas.getTypeError()
print ("Admin1 of Amarillo: " + parent)



