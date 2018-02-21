#-------------------------------------------------------------------------------
# Name:         geocode_with_API
# Purpose:      Accesses a geocoding API (in this case Google) which returns a response
#               in JSON format for each address. The input can be either a text file with
#               one address per line, which will then be converted into a python list (this
#               is commented out), or a python list of addresses typed or pasted into this
#               script. The outputs are 1) a python list of reformatted addresses with latitude
#               and longitude coordinates as well as precision of the geocode match, and
#               2) the same information printed to the python interpreter.
#
#               A large portion of this script was taken from an in-class demonstration by
#               Professor William Drummond at Georgia Institute of Technology, but
#               I have modified it to include both possible methods for inputting addresses,
#               and to address a problem I encountered when executing test runs. The problem is:
#               some addresses at random will return a status "OVER_QUERY_LIMIT" which
#               causes the script to throw an error. I have used if/else statements to
#               tell the script to output NULL instead of the normal outputs when this
#               problem is encountered, and then move on to the next address.
#
# Author:       Matthew Leonard
#
# Created:      02/20/2018
#-------------------------------------------------------------------------------

import urllib, json
import sys, time
import pprint

### specifies name of ascii file with one address or location per line
# addfile = "path/file.txt"

### opens file with addresses and creates list
# addresses = []
# f = open(addfile, 'r')
# for line in f:
#     addresses.append(line)
# f.close()

# or instead of getting addresses from a text file, you can specify addresses here as a list:
addresses = [
   'street, city, state, zip',
   'street, city, state, zip',
   'street, city, state, zip',
   'and so forth'
    ]

quote = '"'
semicolon = ';'

dataout = []
print
print
print
for add in addresses:
    time.sleep(.1)
    prefix = 'https://maps.googleapis.com/maps/api/geocode/json?'
    data = urllib.urlencode({"address" : add})
    url = prefix+data
    #print "url = ", url
    gresp = urllib.urlopen(url)
    jresp = json.loads(gresp.read())
    if jresp['status'] == 'OK':
        lat = jresp['results'][0]['geometry']['location']['lat']
        lon = jresp['results'][0]['geometry']['location']['lng']
        formadd = jresp['results'][0]['formatted_address']
        precision = jresp['results'][0]['geometry']['location_type']
        newloc = [add, formadd.encode('ascii'), lat, lon, precision.encode('ascii')]
        dataout.append(newloc)
        # leading semicolon keeps Excel from removing initial string quote
        print (semicolon+
              quote+add+quote+semicolon+
              quote+formadd+quote+semicolon+
              str(lat)+semicolon+
              str(lon)+semicolon+
              quote+precision+quote)
    else:
        lat = 'NULL'
        lon = 'NULL'
        formadd = 'NULL'
        precision = 'NULL'
        newloc = [add, formadd, lat, lon, precision]
        dataout.append(newloc)
        # leading semicolon keeps Excel from removing initial string quote
        print (semicolon+
              quote+add+quote+semicolon+
              quote+formadd+quote+semicolon+
              quote+lat+quote+semicolon+
              quote+lon+quote+semicolon+
              quote+precision+quote)

