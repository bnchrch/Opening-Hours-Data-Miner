# SENG 474: Data Mining Project Spring 2015

### Objective
To determine the operating hours of buisnesses based on their geographic location and buisness type

### Whats in this repo?
* An exploratory scraper for the google places api written with node
* A final implementation of the scrapper written in threaded python

### What does the scraper do exactly?
* Queries the google places api based on location and either radius or buisness type
** currently it's set to buisness types which are sources from our pre existing database (you can populate it by uncommenting our radius search query)
* then it checks each returned place and will query for further details only if we do not already have the place in our database and the place has opening and closing hours attached
* when it queries for a listings details it will save the results to our postgresql datastore
* if a page token is attached the scraper will query the next page or else it will query a new random location based on the values in location.py

### Technologies Used
* Python 2
* SQL Alchemy
* PostgreSQL
* Weka
* Digital Ocean

### Discoveries
Over 18 days of running we were able to gather 10,657,610 unique data points out of 923,409 locations  when expanding on buisness type and day.

![alt text](https://github.com/bechurch/474project/blob/master/map.png "only 1% of our findings make a population density!")

Using the J48 algorithm in weka we were able to get an accuracy of 80.713%!


### Future Plans
* rewrite the scraper to better handle threading
* save what queries our places data comes from
* make our location selection more intelligent by either storing where we've searched or use a spidering algorithm
* move our findings into a web app
