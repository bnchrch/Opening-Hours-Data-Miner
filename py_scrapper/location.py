from random import randint

#Currently defined to be a random spot in North america (roughly)
def getRandomLoc():
  la = str(randint(31, 55))    #Lat
  lo = str(randint(-126, -65)) #Long

  #Decimal parts of the lat/long ()
  decLa = str(randint(0, 9999))
  decLo = str(randint(0, 9999))

  la = la + "." + decLa
  lo = lo + "." + decLo

  # Return a string in the format of: '48.4222,-123.3657'
  return la + "," + lo
