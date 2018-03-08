import pymysql
import os

workingDirectory = os.path.dirname(os.path.abspath(__file__)) + '/'

pw = open(workingDirectory + 'mariadb/mashup_write','r').readline().rstrip()

# Open a connection to the database
db = pymysql.connect('localhost','mashup_write',pw,'mashup_db',autocommit=True)

# Prepare a cursor object
cursor = db.cursor()


def getSubscriptions(username):
	SQLQuery = 'SELECT HSL_route FROM Subscriptions WHERE Twitter_username="'+username+'";'
	cursor.execute(SQLQuery)
	return cursor.fetchall()

def getSubscribers(HSLRoute):
	SQLQuery = 'SELECT Twitter_username FROM Subscriptions WHERE HSL_route="'+HSLRoute+'";'
	cursor.execute(SQLQuery)
	return cursor.fetchall()

def addSubscription(username, HSLRoute):
	SQLQuery = 'INSERT INTO Subscriptions(Twitter_username, HSL_route) VALUES("'+username+'", "'+HSLRoute+'");'
	cursor.execute(SQLQuery)
	return 

def deleteSubscription(username, HSLRoute):
	SQLQuery = 'DELETE FROM Subscriptions WHERE Twitter_username="'+username+'" AND HSL_route="'+HSLRoute+'";'
	cursor.execute(SQLQuery)
	return

def deleteAllSubscriptions(username):
	SQLQuery = 'DELETE FROM Subscriptions WHERE Twitter_username="'+username+'";'
	cursor.execute(SQLQuery)
	return
