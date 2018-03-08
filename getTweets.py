# This script is responsible for getting the Tweets from the users/ subscribers
# The bot currently supports four commands:
#
# 1. "Subscribe <HSL_route_id>" (example: Subscribe HSL:1023)
# 2. "Unsubscribe <HSL_route_id>" (example: Unsubscribe HSL:1023)
# 3. "Unsubscribe all" (unsubscribes from all routes)
# 4. "Get subscriptions" (get all routes the user has subscribed to)
#
# The script reads incoming tweets and parses them according to the commands
# It will call appropriate functions from database.py, since user data is stored in the DB
# It also calls a Tweet function to inform users that their action has been completed
# Idea: maybe have an option to NOT get a confirmation?


from twitter import getMentions
from pprint import pprint
import os
from pathlib import Path
from database import * # Does this work?

workingDirectory = os.path.dirname(os.path.abspath(__file__)) + '/'

# The ID of the latest Tweet the bot has read in stored in a file
# Here we check whether the file exists
latestTweetIdFileExists = Path(workingDirectory + 'latestTweetId')

# If the file exists, we can go ahead and fetch the latest Id from the file
if (latestTweetIdFileExists.is_file()):
	latestTweetIdFile = open(workingDirectory + 'latestTweetId', 'r')
	latestTweetId = latestTweetIdFile.read()
	latestTweetIdFile.close()
	print('found it')

# If the file does not exists, assume the bot is running for the first time, so it's necessary to get all the Tweets
else:
	latestTweetId = '0'

idList = []
mentions = getMentions(latestTweetId)

for mention in mentions:
	# print(mention.id)
	idList.append(mention.id)
	# print(mention.text)
	tweet = mention.text

	# The keyword for subscribing to new HSL lines is 'subscribe'
	# subscribe is a substring of unsubscribe, so we need to rule that out
	# Could this be done with if elif?
	if 'subscribe' in tweet and 'unsubscribe' not in tweet:
		# After the keyword comes the HSL line, so we split it from the Tweet string
		lineToSubscribe = tweet.split('subscribe ',1)[1]
		print(lineToSubscribe)
		# The user who sent the Tweet, ie. the user who wants to subscribe
		userToSubscribe = mention.user.screen_name
		print(userToSubscribe)
		# Call a subscribe function
	if 'unsubscribe HSL:' in tweet:
		lineToUnsubscribe = tweet.split('unsubscribe ',1)[1]
		userToUnsubscribe = mention.user.screen_name
		# Call an unsubscribe function
	if 'unsubscribe all' in tweet:
		userToUnsubscribe = mention.user.screen_name
		# Call the unsubcribe all function

# We parse the list of Tweet ID's to save the ID of the newest Tweet
# This chould maybe be refactored to the mentions for loop
if len(idList) != 0:
	idList.sort(reverse=True)
	print(idList[0])

	file = open('latestTweetId','w')
	file.write(str(idList[0]))
	file.close()
