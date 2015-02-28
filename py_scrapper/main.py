import threading
import json
import time
from fetch import fetch_remote, fetch_remote_json #For fetching data from url

searchNearbyCmd = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
detailsCmd =      'https://maps.googleapis.com/maps/api/place/details/json?'
api_key = 'AIzaSyBB9KLa1_lrVbPGagttplCeVtoWZ5f0d0o'
req_tally = 0;
has_hours = 0;

class request_details(threading.Thread):
  def __init__ (self, place_id):
    threading.Thread.__init__(self)
    self.place_id = place_id

  def run(self):
    params = {'key' : api_key, 'placeid' : self.place_id}
    json = fetch_remote_json(detailsCmd, params);
    response = json[1]
    print "PID: " + str(self.place_id)
    print response #Do something with this here

class find_places(threading.Thread):
  def __init__ (self, req_url, params, timeout):
    threading.Thread.__init__(self)
    self.req_url = req_url
    self.params = params
    self.timeout = timeout

  def run(self):
    global has_hours, req_tally
    time.sleep(self.timeout)
    print self.req_url
    json = fetch_remote_json(self.req_url, self.params)
    response = json[1]
    results = response['results']
    print 'status:' + response['status']
    token = response.get('next_page_token', 0)
    if token:
      print "Got One: " + token[:64] + "..."
      find_places(searchNearbyCmd, {'pagetoken' : token, 'key' : api_key}, 3).start()

    for res in results:
      if res.get('opening_hours', 0):
        has_hours += 1
        request_details(res['place_id']).start()

    req_tally += len(results)
    print "Req|HasTally: " + str(req_tally) + " | " + str(has_hours)


#Run code here
find_places(searchNearbyCmd, {'key' : api_key,'radius' : '100','location' : '48.4222,-123.3657'}, 0).start()
