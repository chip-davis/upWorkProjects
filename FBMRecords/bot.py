import tweepy
import json
import sys

# api keys to authenticate with twitter API
CONSUMER_KEY        = ""
CONSUMER_SECRET     = ""
ACCESS_TOKEN        = ""
ACCESS_TOKEN_SECRET = ""

#empty list to contain UIDS of users
UIDS = []

#key words to search for in possible tweets
KEYWORDS            = ["@nba_topshot", "moments", "moment", "my showcase", "my showcases", "Witness history", "pack",
                       "packs", "top shot", "nba top shot", "topshot"]


#adds all of the userIDS of the users we are tracking to list
with open (r"UIDS.txt", 'r') as f:
    for line in f:
        UIDS.append(line.strip())

#converts UIDS to a set so the running time of a lookup is O(1) not 0(n)
UIDS = set(UIDS)

#tweepy class to create and listen to a stream
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        #grabs who the tweet is from to determine if it actually came from one of the followed accounts
        tweetFromUID           = (tweet.user.id_str)
        #sets a default value for repliedToTweetContents so there is no error in the case
        #that a tweet is not a reply
        repliedToTweetContents = ""
        
        #checks that the tweet is origniating from one of the selected UIDs
        if (tweetFromUID in UIDS):
            #if the tweet is a reply and or retweet
            if (tweet.in_reply_to_status_id_str is not None):
                #get the ID of the parent tweet (the one the user is replying to)
                repliedToTweet         = tweet.in_reply_to_status_id_str
                #actually get the tweet status
                repliedToTweetContents = api.get_status(repliedToTweet)
                #gets the tweet text can now move on to the next check
                repliedToTweetContents = repliedToTweetContents.text

            for word in KEYWORDS:
                #checks to see if either the tweet or the tweet being replied to contains any of the keywords
                if word.lower() in tweet.text.lower() or word.lower() in repliedToTweetContents.lower():
                    tweetID = tweet.id
                    try:
                        #retweets the selected tweet
                        print(f"Match {tweet.text}. Retweeting...")
                        api.retweet(tweetID)
                    except:
                        print("There was an error.")

    def on_error(self, status):
        print("Error detected")

#creates new tweepy instance that is logged in with our api keys
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#creates our actualy tweepy api object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#sets up the stream with the selected UIDS
tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(follow=UIDS, is_async=True)