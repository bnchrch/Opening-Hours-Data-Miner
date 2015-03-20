#Simple script for converting the results CSV file
#To one useable with weka. Also rounds all times to
#the nearest half an hour, and saves them as discrete
#values (48 total, 0000, 0030, 0100, 0130, ... 2330)
#Padded with 0's


#Given format HHMM - too lazy to rewrite this function. No need to do it. Works as it. :D
def convertTime(time):
  numHours = 0

  while(time > 100) :
    time -= 100
    numHours += 1

  #Round to nearest half an hour
  if(time >= 15 and time < 45):
    time = 30
  else:
    time = 0

  #Convert the time
  time = time + 100 * numHours
  return time



#Convert the file to the correct format
print("Opening file for writing converting")
fin = open("in.csv", "r")
fout = open("out.csv", "w")
fout.write("place_id,rating,lat,long,day,open_time,close_time,type_title_list\n") #Write header to file

line = fin.readline()
print ("HEADER: "+ line)
line = fin.readline()
while(len(line)):
  arr = line.split(",")
  print ("Conv: "+str(arr))

  #Open & close time past format: (HHMM), or leave blank if missing
  if len(arr[5]):
    openTime = int(arr[5])
    openTime = convertTime(openTime)
  else:
    openTime = ''

  if len(arr[6]):
    closeTime = int(arr[6])
    closeTime = convertTime(closeTime)
  else:
    closeTime = ''

  #Surround open+close times in quotes (turn them into discreet values instead of continuous [harder to work with])
  oTime = str(openTime).zfill(4)
  cTime = str(closeTime).zfill(4)
  oTime = oTime[:2] + ":" + oTime[2:]
  cTime = cTime[:2] + ":" + cTime[2:]
  fout.write(arr[0].strip()+','+arr[1].strip()+','+arr[2].strip()+','+arr[3].strip()+','+arr[4].strip()+',"'+oTime+'","'+cTime+'",'+arr[7].strip()+'\n')

  line = fin.readline()

fin.close()
fout.close()
print "All done this stuff"