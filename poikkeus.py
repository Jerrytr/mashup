import requests
import json
from pprint import pprint
from twitter import tweet

url = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
payload = open('request.json')
headers = {'Content-Type': 'application/graphql'}
r = requests.post(url=url, data=payload, headers=headers)
jsonstuff = r.content
data = json.loads(jsonstuff)
# pprint(data['data']['alerts'][0]['alertDescriptionText'])
# pprint(data['data']['alerts'][0]['route']['gtfsId'])
# mystuff = data['data']['alerts'][0]['route']['gtfsId']

routeID = data['data']['alerts'][0]['route']['gtfsId']
disruptDesc = data['data']['alerts'][0]['alertDescriptionText']

metrolines = ['HSL:31M1', 'HSL:31M1B', 'HSL:31M2', 'HSL:31M2B']
print(routeID)
if (routeID in metrolines):
	print('metro is broken again')
	tweet('@Jers1_ ' + disruptDesc[0:132])
else:
	print('metro works')

