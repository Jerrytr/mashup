import os
import requests
import json
from pprint import pprint
from twitter import tweet

metrolines = ['HSL:31M1', 'HSL:31M1B', 'HSL:31M2', 'HSL:31M2B']

workingDirectory = os.path.dirname(os.path.abspath(__file__)) + '/'
url = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
payload = open(workingDirectory + 'request.json')
headers = {'Content-Type': 'application/graphql'}
r = requests.post(url=url, data=payload, headers=headers)
jsonResponse = r.content
result = json.loads(jsonResponse)
# pprint(data['data']['alerts'][0]['alertDescriptionText'])
# pprint(data['data']['alerts'][0]['route']['gtfsId'])
# mystuff = data['data']['alerts'][0]['route']['gtfsId']

disruptions = result['data']['alerts']
if (len(disruptions) == 0):
	print('no disruptions whatsoever')
else:
	for i in range(0, len(disruptions)):
		routeID = disruptions[i]['route']['gtfsId']
		disruptDesc = disruptions[i]['alertDescriptionText']
		print(routeID)
		if (routeID in metrolines):
			print('metro is broken again')
			tweet('@Jers1_ ' + disruptDesc[0:132])
		else:
			print('metro works')
# routeID = result['data']['alerts'][0]['route']['gtfsId']
# disruptDesc = result['data']['alerts'][0]['alertDescriptionText']
