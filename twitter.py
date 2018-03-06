import tweepy
import os

workingDirectory = os.path.dirname(os.path.abspath(__file__)) + '/'

consumer_key = open(workingDirectory + 'keys/consumer_key','r').readline().rstrip()
consumer_secret = open(workingDirectory + 'keys/consumer_secret','r').readline().rstrip()
access_token = open(workingDirectory + 'keys/access_token','r').readline().rstrip()
access_token_secret = open(workingDirectory + 'keys/access_token_secret','r').readline().rstrip()

def OAuth(consumer_key, consumer_secret, access_token, access_token_secret):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	return auth

def apiAuth(auth):
	api = tweepy.API(auth)
	return api

auth = OAuth(consumer_key, consumer_secret, access_token, access_token_secret)
api = apiAuth(auth)

def tweet(stuff):
	api.update_status(stuff)

def getMentions(latestId):
	return api.search(q='@mashbot001', since_id=latestId)
	
# api.update_status('multi-functional')
