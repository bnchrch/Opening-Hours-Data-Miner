#Simple script for converting the results CSV file
#To one useable with weka. Also rounds all times to
#the nearest half an hour, and saves them as discrete
#values (48 total, 0000, 0030, 0100, 0130, ... 2330)
#Padded with 0's


#Given format HHMM - too lazy to rewrite this function. No need to do it. Works as it. :D

#Convert the file to the correct format
print("Opening file for writing converting")
fin = open("in.csv", "r")
fout = open("out.csv", "w")
fout.write("place_id,rating,lat,long,day,open_time,close_time,type_title_list\n") #Write header to file

line = fin.readline()
print ("HEADER: "+ line)
line = fin.readline()
while(len(line)):
  arr = line.split(";")
  print ("Conv: "+str(arr))

  #Surround open+close times in quotes (turn them into discreet values instead of continuous [harder to work with])
  newArr = arr[7].split(",");
  for val in newArr:
    fout.write(arr[0].strip()+','+arr[1].strip()+','+arr[2].strip()+','+arr[3].strip()+','+arr[4].strip()+','+arr[5].strip()+','+arr[6].strip()+','+val.strip()+'\n')

  line = fin.readline()

fin.close()
fout.close()
print "All done this stuff"