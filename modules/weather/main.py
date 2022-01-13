import requests
import time
from modules.utils import ghc, project

module = ghc.Module(project.ModuleType.WEATHER, project.Paths.API_URL.value, project.Paths.WEBSOCKET_URL.value)
api_key = ''
lat = 0
lon = 0

@module.listening('api-key')
def api_key_listener(data):
  global api_key
  api_key = data['apiKey']
  print('New API key defined :', data['apiKey'])

@module.listening('location')
def api_key_listener(data):
  global lat, lon
  lat = data['lat']
  lon = data['lon']
  print('New location defined :', data['lat'], data['lon'])

def update():
  while module.connected:
    if api_key and lat and lon:
      res = requests.get('http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=' + api_key + '&q=' + str(lat) + ',' + str(lon))
      res = requests.get('http://dataservice.accuweather.com/currentconditions/v1/' + res.json()['Key'] + '?apikey=' + api_key)
      module.send('weather', res.json()[0]['Temperature']['Metric'])
      time.sleep(1800)
    else:
      time.sleep(10)

module.connect()
module.run_task(update)
module.wait()
