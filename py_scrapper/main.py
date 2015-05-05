import threading
import json
import time
from fetch import fetch_remote, fetch_remote_json
from location import getRandomLoc, get_location_from_results
from models import PlacesPipeline, PlaceDetails

searchNearbyCmd = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
detailsCmd = 'https://maps.googleapis.com/maps/api/place/details/json?'

db = PlacesPipeline()
#List of all api keys
apiKeys = [] 
#Non atomic operations need to be thread safe!
#When something is required to be thread safe, call with globalLock:
globalLock = threading.Lock()


class request_details(threading.Thread):
    """
    threaded api querier for places/details
    """
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
        #print "Response: " + str(response.get('result', 'NOTHING FOUND'))[:100]+"..." #For debugging dont display the whole string


class find_places(threading.Thread):
    """
    threaded api querier for /places
    """
    def __init__(self, req_url, apiKey, params, timeout):
        threading.Thread.__init__(self)
        self.req_url = req_url
        self.params = params
        self.timeout = timeout
        self.apiKey = apiKey

    def run(self):
        time.sleep(self.timeout)
        json = fetch_remote_json(self.req_url, self.params)
        response = json[1]
        results = response.get('results', [])
        print 'status: ' + response['status']
        if response['status'] != 'OVER_QUERY_LIMIT':
            token = response.get('next_page_token', 0)

            if token: #There is a token (data gets sent in 3 pages, so request data for next page)
                print "Token Found: " + token[:64] + "..."
                find_places(searchNearbyCmd, self.apiKey, {'key': self.apiKey, 'radius': '10000', 'location': getRandomLoc()}, 3).start()
                #find_places(searchNearbyCmd, self.apiKey, {'pagetoken' : token, 'key' : self.apiKey}, 3).start()
            else:
                #No token exists, randomly grab another spot and get the information around it.
                print 'No Token, Relocating Search'
                find_places(searchNearbyCmd, self.apiKey, {'key': self.apiKey, 'radius': '10000', 'location': getRandomLoc()}, 3).start()
                #find_places(searchNearbyCmd, self.apiKey, {'key': self.apiKey, 'rankby': 'distance', 'types': db.get_type_string_for_query(), 'location': getRandomLoc()}, 3).start()

            cnt = 0
            for res in results:
                # check the database for id
                if db.get_details_by_id(res['place_id']) is None:
                    print 'got unique result'
                    print res.get('opening_hours', 0)
                    print res
                    if res.get('opening_hours', False):
                        cnt += 1
                        print 'has opening hours'
                        request_details(self.apiKey, res['place_id']).start()
                else:
                    print 'not new'


def main():
    for key in apiKeys:
        find_places(searchNearbyCmd, key, {'key': key, 'radius': '10000', 'location': getRandomLoc()}, 3).start()
        #find_places(searchNearbyCmd, key, {'key': key, 'rankby': 'distance', 'types': db.get_type_string_for_query(),'location' : getRandomLoc()}, 0).start()

if __name__ == "__main__":
    main()
