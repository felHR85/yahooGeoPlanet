#-*- coding: utf-8 -*-
import yahooGeoPlanet

yahooId = "YOUR YAHOO ID"

geoPlanet = yahooGeoPlanet.yahooGeoPlanet(yahooId) # Instantiate a yahooGeoPlanet object
geoPlanet.setLang("en") # set language to english
madrid = geoPlanet.getWoeidByPlace('Madrid')
barcelona = geoPlanet.getWoeidByPlace("Barcelona")  # get two place objects with data of Madrid and Barcelona

# if isinstance(madrid,yahooGeoError):
# 	print madrid.getTypeError if we get an error
# else:

""" Get some information of each object: Woeid code, country of the place, kind of administration, uri of the data and the latitude of Madrid."""
woeidM = madrid[0].getWoeid()
countryM = madrid[0].getCountry()
uriM = madrid[0].getUri()
admin1M = madrid[0].getAdmin1()
latitudM = madrid[0].getCentroid().getLatitude()

woeidB = barcelona[0].getWoeid()
countryB = barcelona[0].getCountry()
uriB = barcelona[0].getUri()
admin1B = barcelona[0].getAdmin1()
admin1AttrB = barcelona[0].getAdmin1Attrs().getType()



""" Print Data """

print "Woeid of Madrid: " + str(woeidM) + " Country of Madrid : " + str(countryM) + " Uri: " + str(uriM) + " admin1: " + str(admin1M) + " latitude: " + str(latitudM)
print " "
print " "
print "Woeid of Barcelona: " + str(woeidB) + " Country of Barcelona: " + str(countryB) + " Uri: " + str(uriB) + " admin1: " + str(admin1B) + " admin1 attributes: " + str(admin1AttrB)
print " "
print " "


""" Now We check if we have a valid Woeid we can get information """
newPlace = geoPlanet.getPlaceByWoeid(2397733)
# print newPlace.getTypeError() if we get an error

city = newPlace.getName()
woeidB = newPlace.getWoeid()
countryB = newPlace.getCountry()
uriB = newPlace.getUri()
admin1B = newPlace.getAdmin1()
admin1AttrB = newPlace.getAdmin1Attrs().getType()
print "Woeid 2397733: " + str(city) + " WOEID code: " + str(woeidB) + " Country: " + str(countryB) + " Uri: " + str(uriB) + " admin1: " + str(admin1B) + " admin1 atributos: " + str(admin1AttrB)
print " "
print " "

""" We need to know the parent Woeid code of a given woeid which we know it is from Amarillo. Where is Amarillo? """
amarilloTexas = geoPlanet.getParentWoeid(12792500)

parent = amarilloTexas.getAdmin1()
# print amarilloTexas.getTypeError()
print "Admin1 of Amarillo: " + str(parent)



