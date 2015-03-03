import threading
import json
import time
from fetch import fetch_remote, fetch_remote_json
from location import getRandomLoc
from models import PlacesPipeline, PlaceDetails

searchNearbyCmd = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
detailsCmd = 'https://maps.googleapis.com/maps/api/place/details/json?'
req_tally = 0
has_hours = 0

db = PlacesPipeline()
#List of all api keys. We should all get one if possible
apiKeys = ['AIzaSyBB9KLa1_lrVbPGagttplCeVtoWZ5f0d0o','AIzaSyAMWj290YncOAX-gXT7MIYVe6bFrFJiNV0','AIzaSyDh5XIIfk9r-g_Gb-wcgqehv-0CNkRNfgg']

#Non atomic operations need to be thread safe!
#When something is required to be thread safe, call with globalLock:
globalLock = threading.Lock()


def incReqTally(amt):
    with globalLock:
        global req_tally
        req_tally += amt


def incHasHours(amt):
    with globalLock:
        global has_hours
        has_hours += amt


class request_details(threading.Thread):
  def __init__ (self, apiKey, place_id):
    threading.Thread.__init__(self)
    self.place_id = place_id
    self.apiKey = apiKey

  def run(self):
    params = {'key' : self.apiKey, 'placeid' : self.place_id}
    json = fetch_remote_json(detailsCmd, params);
    response = json[1]
    result = response.get('result', 'NOTHING FOUND')
    if result:
        db.process_details(result)
    #Do something with placeId and response here
    #print "Response: " + str(response.get('result', 'NOTHING FOUND'))[:100]+"..." #For debugging dont display the whole string

class find_places(threading.Thread):
  def __init__ (self, req_url, apiKey, params, timeout, original_params=None):
    threading.Thread.__init__(self)
    self.req_url = req_url
    self.params = params
    self.timeout = timeout
    self.apiKey = apiKey

  def run(self):
    global has_hours, req_tally
    time.sleep(self.timeout)
    json = fetch_remote_json(self.req_url, self.params)
    response = json[1]
    results = response.get('results', [])
    print 'status: ' + response['status']
    if response['status'] != 'OVER_QUERY_LIMIT':
        token = response.get('next_page_token', 0)

        if token: #There is a token (data gets sent in 3 pages, so request data for next page)
          print "Token Found: " + token[:64] + "..."
          find_places(searchNearbyCmd, self.apiKey, {'pagetoken' : token, 'key' : self.apiKey}, 3).start()
        else:
          #No token exists, randomly grab another spot and get the information around it.
          print 'No Token, Relocating Search'
          find_places(searchNearbyCmd, self.apiKey, {'key' : self.apiKey, 'radius' : '25000' , 'location' : getRandomLoc()}, 3).start()

        cnt = 0
        for res in results:
          if res.get('opening_hours', 0):
            cnt += 1
          if db.get_details_by_id(res['place_id']) is None:
            request_details(self.apiKey, res['place_id']).start()
          else:
            print 'not new'
        incHasHours(cnt) #intentionally using a cnter to avoid unneeded locks + unlocks
        print "With|Out Hours: " + str(cnt) + " | " + str(len(results) - cnt)

        incReqTally(len(results))
        print "Req|HasTally: " + str(req_tally) + " | " + str(has_hours)



def main():
    for key in apiKeys:
        find_places(searchNearbyCmd, key, {'key' : key, 'radius' : '25000' , 'location' : getRandomLoc()}, 0).start()

if __name__ == "__main__":
    main()
