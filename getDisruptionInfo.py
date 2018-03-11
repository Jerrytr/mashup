import os
import requests
import json
from pprint import pprint
from twitter import sendTweet
from database import *

# metrolines = ['HSL:31M1', 'HSL:31M1B', 'HSL:31M2', 'HSL:31M2B']

workingDirectory = os.path.dirname(os.path.abspath(__file__)) + '/'
url = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
# request.json contains the parameters we send to the HSL API
payload = open(workingDirectory + 'request.json')
headers = {'Content-Type': 'application/graphql'}
r = requests.post(url=url, data=payload, headers=headers)
jsonResponse = r.content
result = json.loads(jsonResponse)

# The essential part of the API response
disruptions = result['data']['alerts']
if (len(disruptions) == 0):
	print('no disruptions whatsoever')
else:
	for i in range(0, len(disruptions)):

		# The ID of the route, same as users have subscriptions to in the database
		routeID = disruptions[i]['route']['gtfsId']

		# Information about the disruption, bus cancelled, how long the disruption lasts etc.
		disruptDesc = disruptions[i]['alertDescriptionText']
		print(routeID)

		# Get the users we need to notify about this line
		usersToNotify = []
		rawUsersToNotify = getSubscribers(routeID)
		for i in rawUsersToNotify:
			usersToNotify.append(i[0])
		
		# Notify the users
		for i in usersToNotify:
			tweetPhrase = '@'+i+disruptDesc
			sendTweet(tweetPhrase)

		# Legacy code
		# if (routeID in metrolines):
		#	print('metro is broken again')
		#	sendTweet('@Jers1_ ' + disruptDesc[0:132])
		#else:
		#	print('metro works')
# routeID = result['data']['alerts'][0]['route']['gtfsId']
# disruptDesc = result['data']['alerts'][0]['alertDescriptionText']

