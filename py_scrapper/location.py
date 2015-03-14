from random import randint, choice

#not in use...
def get_location_from_results(results):
    result = choice(results)
    lat = result.get('geometry', {}).get('location', {}).get('lat', {})
    lng = result.get('geometry', {}).get('location', {}).get('lng', {})
    if lat and lng:
        return str(lat) + "," + str(lng)
    else:
        return getRandomLoc()

#Currently defined to be a random spot in North america (roughly)
def getRandomLoc():
  la = str(randint(37, 52))    #Lat
  lo = str(randint(-4, 24)) #Long

  #Decimal parts of the lat/long ()
  decLa = str(randint(0, 9999))
  decLo = str(randint(0, 9999))

  la = la + "." + decLa
  lo = lo + "." + decLo

  # Return a string in the format of: '48.4222,-123.3657'
  return la + "," + lo
