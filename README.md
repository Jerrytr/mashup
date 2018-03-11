# mashup-backend

This is the backend part of the mashup project. This part takes care of storing subscriptions, checking for disruptions and informing subscribers of the disruptions.

The different files:
- database.sql is used to initially create the database. Usernames and password are your own business, so those are not included
- request.json contains the parameters needed to query the HSL API for disruptions
- database.py contains functions for checking and updating the database of subscribers
- twitter.py contains functions for sending and checking for Tweets
- getDisruptionInfo.py queries the HSL API for disruptions and notifies subscribers
- getTweets.py queries the Twitter API for new subscribers and unsubscribers and sends confirmation Tweets
