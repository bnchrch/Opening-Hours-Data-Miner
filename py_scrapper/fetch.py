import json
import urllib
import urllib2

def fetch_remote(service_url, params={}, use_http_post=False):
  encoded_data = {}
  for k, v in params.items():
    if type(v) in [str, unicode]:
      v = v.encode('utf-8')
    encoded_data[k] = v
  encoded_data = urllib.urlencode(encoded_data)

  if not use_http_post:
    query_url = (service_url if service_url.endswith('?') else '%s?' % service_url)
    request_url = query_url + encoded_data
    request = urllib2.Request(request_url)
  else:
    request_url = service_url
    request = urllib2.Request(service_url, data=encoded_data)
  return (request_url, urllib2.urlopen(request))

def fetch_remote_json(service_url, params={}, use_http_post=False):
  request_url, response = fetch_remote(service_url, params, use_http_post)
  return (request_url, json.load(response))