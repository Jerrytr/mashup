# The functions in this script are called by another script
# The Database format is following:
#
# Twitter_username		HSL_route
# user01				HSL:0000
# user01				HSL:1111
# user02				HSL:0000
# user03				HSL:4413

# And so on...

import pymysql
import os

workingDirectory = os.path.dirname(os.path.abspath(__file__)) + '/'

pw = open(workingDirectory + 'mariadb/mashup_write','r').readline().rstrip()

# Open a connection to the database
# Enable autocommit to make changes instant
# BTW all this needs to be a function that gets called by each of the subscription functions
# So maybe do that...
db = pymysql.connect('localhost','mashup_write',pw,'mashup_db',autocommit=True)

# Prepare a cursor object
cursor = db.cursor()

# Get all the HSL Routes a user
def getSubscriptions(username):
	SQLQuery = 'SELECT HSL_route FROM Subscriptions WHERE Twitter_username="'+username+'";'
	cursor.execute(SQLQuery)
	return cursor.fetchall()

# Get all the subscribers for an HSL route
def getSubscribers(HSLRoute):
	SQLQuery = 'SELECT Twitter_username FROM Subscriptions WHERE HSL_route="'+HSLRoute+'";'
	cursor.execute(SQLQuery)
	return cursor.fetchall()

def checkSubscription(username, HSLRoute):
	SQLQuery = 'SELECT * FROM Subscriptions WHERE Twitter_username="'+username+'" AND HSL_route="'+HSLRoute+'";'
	cursor.execute(SQLQuery)
	cursor.fetchall()
	print(cursor.rowcount)
	if cursor.rowcount == 0:
		return False
	else:
		return True


# Add a certain user as an subscriber to a certain HSL route
def addSubscription(username, HSLRoute):
	# Only subscribe if the user hasn't subscribed to that HSL route yet
	if not checkSubscription(username, HSLRoute):
		SQLQuery = 'INSERT INTO Subscriptions(Twitter_username, HSL_route) VALUES("'+username+'", "'+HSLRoute+'");'
		cursor.execute(SQLQuery)
	return 

# Delete a certain user's subscription of a certain HSL route
def deleteSubscription(username, HSLRoute):
	SQLQuery = 'DELETE FROM Subscriptions WHERE Twitter_username="'+username+'" AND HSL_route="'+HSLRoute+'";'
	cursor.execute(SQLQuery)
	return

# Delete a certain user's all subscriptions
def deleteAllSubscriptions(username):
	SQLQuery = 'DELETE FROM Subscriptions WHERE Twitter_username="'+username+'";'
	cursor.execute(SQLQuery)
	return
