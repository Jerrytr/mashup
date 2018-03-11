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
from twitter import sendTweet
from pprint import pprint
import os
from pathlib import Path
from database import *

workingDirectory = os.path.dirname(os.path.abspath(__file__)) + '/'

# The ID of the latest Tweet the bot has read is stored in a file
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
	idList.append(mention.id)
	tweet = mention.text

	# The keyword for subscribing to new HSL lines is 'subscribe'
	# subscribe is a substring of unsubscribe, so we need to rule that out
	# Could this be done with if elif?
	if 'subscribe' in tweet and 'unsubscribe' not in tweet:

		# The HSL line number comes after the keyword, so we split it from the Tweet string
		lineToSubscribe = tweet.split('subscribe ',1)[1]

		# The user who sent the Tweet, ie. the user who wants to subscribe
		userToSubscribe = mention.user.screen_name

		# Call the subscribe function from database.py
		print(userToSubscribe+' wants to subscribe to '+lineToSubscribe)
		addSubscription(userToSubscribe, lineToSubscribe)
		
		# Send out a tweet to let the user know we didn't ignore them :)
		tweetPhrase = '@'+userToSubscribe+', you have subscribed to '+lineToSubscribe
		sendTweet(tweetPhrase)

	if 'unsubscribe HSL:' in tweet:
		lineToUnsubscribe = tweet.split('unsubscribe ',1)[1]
		userToUnsubscribe = mention.user.screen_name

		# Call the unsubscribe function from database.py
		deleteSubscription(userToUnsubscribe, lineToUnsubscribe)
		tweetPhrase = '@'+userToUnsubscribe+', you have unsubscribed from '+lineToUnsubscribe
		sendTweet(tweetPhrase)

	if 'unsubscribe all' in tweet:
		userToUnsubscribe = mention.user.screen_name

		# Call the unsubcribe all function from database.py
		deleteAllSubscriptions(userToUnsubscribe)
		tweetPhrase = '@'+userToUnsubscribe+', you have unsubscribed from all HSL lines.'
		sendTweet(tweetPhrase)

	if 'get subscriptions' in tweet:
		subscriptions = []
		userToGetSubscriptions = mention.user.screen_name

		# Call the getSubscriptions function from database.py
		rawSubscriptions = getSubscriptions(userToGetSubscriptions)
		for row in rawSubscriptions:
			subscriptions.append(row[0])
		print(subscriptions)
		tweetPhrase = '@'+userToGetSubscriptions+', you are subscribed to '
		for i in subscriptions:
			tweetPhrase += i+' '
		print(tweetPhrase)
		sendTweet(tweetPhrase)

# We parse the list of Tweet ID's to save the ID of the newest Tweet
# This chould maybe be refactored to the mentions for loop
if len(idList) != 0:
	idList.sort(reverse=True)
	print(idList[0])

	file = open(workingDirectory+'latestTweetId','w')
	file.write(str(idList[0]))
	file.close()
