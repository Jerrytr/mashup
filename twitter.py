import tweepy

consumer_key = open('keys/consumer_key','r').readline().rstrip()
consumer_secret = open('keys/consumer_secret','r').readline().rstrip()
access_token = open('keys/access_token','r').readline().rstrip()
access_token_secret = open('keys/access_token_secret','r').readline().rstrip()

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
# api.update_status('multi-functional')