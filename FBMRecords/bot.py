import tweepy
from tweepy.error import TweepError
from queue import Queue
from threading import Thread
# api keys to authenticate with twitter API

CONSUMER_KEY        = ""
CONSUMER_SECRET     = ""
ACCESS_TOKEN        = ""
ACCESS_TOKEN_SECRET = " "

#key words to search for in possible tweets
PLAYER_KEYWORDS            = ["@nba_topshot", "my showcase", "my showcases", "Witness history", "pack",
                            "packs", "top shot", "nba top shot", "topshot", "#nbatopshot", "#topshot",
                            "https://nbatopshot.com/", "@nbatopshot", "moment", "moments", "showcase", 
                             "showcases", "my showcase"]

TEAM_KEYWORDS              = ["@nba_topshot", "Witness history","packs", "top shot", "nba top shot", 
                            "topshot", "#nbatopshot", "#topshot","https://nbatopshot.com/", "@nbatopshot"]

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, q=Queue()):
        super(MyStreamListener, self).__init__()
        super().__init__()
        self.q = q
        for i in range(4):
            t = Thread(target=self.process)
            t.daemon = True
            t.start()

    def on_status(self, data):
        self.q.put(data)
    
    def process(self):
        while True:
            status = self.q.get()
            
            tweetText       = status.text
            tweetFrom       = status.user.id_str
            tweetID         = status.id
            inReplyToTweet  = status.in_reply_to_status_id_str
            
            if (tweetFrom in teamUIDS):

                if(inReplyToTweet != None):
                    replyToTweetText = api.get_status(inReplyToTweet)
                    replyToTweetText = replyToTweetText.text

                    for word in replyToTweetText.split():
                        for keyword in TEAM_KEYWORDS:
                            if word.lower() == keyword.lower():
                                try:
                                    print(f"Match: {replyToTweetText}. Retweeting...")
                                    api.retweet(tweetID)
                                except tweepy.TweepError as ex:
                                    print(f"Tweepy error: {ex}")
                                except:
                                    print("Other error.")


                for word in tweetText.split():
                    for keyword in TEAM_KEYWORDS:
                        if word.lower() == keyword.lower():
                            try:
                                print(f"Match: {tweetText}. Retweeting...")
                                api.retweet(tweetID)
                            except tweepy.TweepError as ex:
                                print(f"Tweepy error: {ex}")
                            except:
                                print("Other error.")
            if (tweetFrom in playerUIDS):

                if(inReplyToTweet != None):
                    replyToTweetText = api.get_status(inReplyToTweet)
                    replyToTweetText = replyToTweetText.text
                    for keyword in PLAYER_KEYWORDS:
                        if(keyword.lower()) in replyToTweetText.lower():
                            try:
                                print(f"Match {replyToTweetText} from player {tweetFrom}. Retweeting...")
                                api.retweet(tweetID)
                            except tweepy.TweepError as ex:
                                print(f"Tweepy error: {ex}")
                            except:
                                print("Other error")
                for keyword in PLAYER_KEYWORDS:
                    if keyword.lower() in tweetText.lower():
                        try:
                            print(f"Match {tweetText} from player {tweetFrom}. Retweeting...")
                            api.retweet(tweetID)
                        except tweepy.TweepError as ex:
                            print(f"Tweepy error: {ex}")
                        except:
                            print("Other error")



            self.q.task_done()



    def on_error(self, status_code):
        if status_code == 420:
            return True
        else:
            return True


def getUIDS():
    global playerUIDS, teamUIDS, UIDS
    playerUIDS = []
    teamUIDS   = []
    UIDS       = {}

    #adds all of the userIDS of the users we are tracking to list
    with open (r"playerUIDS.txt", 'r') as f:
        for line in f:
            playerUIDS.append(line.strip())
    #converts UIDS to a set so the running time of a lookup is O(1) not 0(n)
    playerUIDS = set(playerUIDS)

    with open(r"teamsUIDS.txt", 'r') as f:
        for line in f:
            teamUIDS.append(line.strip())
    
    teamUIDS = set(teamUIDS)
    UIDS = playerUIDS.union(teamUIDS)

    

def getAPI():
    global api
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    #creates our actualy tweepy api object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    return(api)


def main():
    getUIDS()
    api = getAPI()
    print("Starting...")
    
    myStreamListener = MyStreamListener()
    while True:
        try:
            myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
            myStream.filter(follow=UIDS, stall_warnings=True)
        except:
            print("uh oh")

main()