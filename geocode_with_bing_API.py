#-------------------------------------------------------------------------------
# Name:         geocode_with_bing_API
#
# Purpose:      Accesses a geocoding API (in this case Bing) which returns a response
#               in JSON format for each address. The input should be a CSV file,
#               with columns/fields named 'Name', 'Zip', 'City', and 'Address' (or if your
#               input file has different field names, you can modify the scrip to specify
#               those as needed. For each line in the CSV file, the script constructs a URL
#               to submit to the Bing geocoding API.
#
#               The outputs are 1) a python list of locations (dataout), each of which is a list
#               containing location name, original address, reformatted addresses, latitude,
#               longitude, and precision and confidence of the geocode match; and
#               2) the same information printed to the python interpreter.
#
#               I have used if/else statements to tell the script to output the above
#               if the status of the response is 'OK', and otherwise to output 'NULL' values
#               and status codes when a status other than 'OK' is returned, and then move on
#               to the next address. So far, each address I've tested has returned status 'OK'.
#
# Author:       Matthew Leonard
#
# Created:      03/27/2018
#-------------------------------------------------------------------------------

import urllib, json
import sys, time
import pprint
import arcpy
import csv

nameList = []
zipList = []
cityList = []
addressList = []

# specify the path of your input file here as a string (this script uses .csv as the input file type).
with open('C:/path/file.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nameList.append(row['Name'])
        zipList.append(row['Zip'])
        cityList.append(row['City'])
        addressList.append(row['Address'])

# The field names specified above ('Name', 'Zip', 'City', and 'Address') came from the particular csv file that was used for testing.
# If this is to be used as an ArcGIS tool, then they will need to be replaced with parameters to be specified by the user
# (as well as the csv input file).

quote = '"'
semicolon = ';'

dataout = []
print
print
print

BingMapsKey = 'YourKeyHere'
# Insert your Bing Maps Key (this is required to use the Bing geocoding service and can be obtained for free)

indexCount = 0

for add in addressList:

# example bing unstructured URL (code below constructs URL using the following format):
# http://dev.virtualearth.net/REST/v1/Locations?countryRegion=countryRegion&adminDistrict=adminDistrict& [end of prefix] locality=locality&postalCode=postalCode&addressLine=addressLine [begin suffix] &userLocation=userLocation&userIp=userIp&usermapView=usermapView&includeNeighborhood=includeNeighborhood&maxResults=maxResults&key=BingMapsKey

    prefix = 'http://dev.virtualearth.net/REST/v1/Locations?countryRegion=US&adminDistrict=GA&'
    # assuming all addresses are in GA.

    name = nameList[indexCount]

    zipCode = urllib.urlencode({"postalCode" : zipList[indexCount]})
    city = urllib.urlencode({"locality" : cityList[indexCount]})
    address = urllib.urlencode({"addressLine" : add})

    data = zipCode+"&"+city+"&"+address
    suffix = "&maxResults=1&key="+BingMapsKey
    url = prefix+data+suffix

    bresp = urllib.urlopen(url)
    jresp = json.loads(bresp.read())
    if jresp['statusDescription'] == 'OK':
        lat = jresp['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates'][0]
        lon = jresp['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates'][1]
        formadd = jresp['resourceSets'][0]['resources'][0]['address']['formattedAddress']
        precision = jresp['resourceSets'][0]['resources'][0]['geocodePoints'][0]['calculationMethod']
        confidence = jresp['resourceSets'][0]['resources'][0]['confidence']
        statusCode = jresp['statusCode']
        status = jresp['statusDescription']

        newloc = [name, add, formadd.encode('ascii'), lat, lon, precision.encode('ascii'), confidence.encode('ascii')]
        dataout.append(newloc)
        # leading semicolon keeps Excel from removing initial string quote
        print (semicolon+
            quote+name+quote+semicolon+
            quote+add+quote+semicolon+
            quote+formadd+quote+semicolon+
            str(lat)+semicolon+
            str(lon)+semicolon+
            quote+precision+quote+semicolon+
            quote+confidence+quote)
    else:
        lat = 'NULL'
        lon = 'NULL'
        formadd = 'NULL'
        precision = 'NULL'
        confidence = 'NULL'
        newloc = [name, add, formadd.encode('ascii'), lat, lon, precision.encode('ascii'), confidence.encode('ascii')]
        dataout.append(newloc)
        # leading semicolon keeps Excel from removing initial string quote
        print (semicolon+
            quote+name+quote+semicolon+
            quote+add+quote+semicolon+
            quote+formadd+quote+semicolon+
            quote+precision+quote+semicolon+
            quote+confidence+quote+semicolon+
            quote+"Status: "+status+quote+semicolon+
            quote+"Status code: "+statusCode+quote)
    time.sleep(.1)
    # pause between requests...check the requests per second (and per day) limit for Bing if you need to
    # geocode large numbers of addresses, and adjust this as necessary...

    indexCount += 1
    # this part is crucial for constructing the correct Bing URL for each request!!!
