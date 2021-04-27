# import the module
import tweepy
import csv
import datetime
  
# assign the values accordingly
access_token = "1381898922491326464-n1E7nKRAoU1CVOWbW4mGeJWvHQTNkS"
access_token_secret = "wg5ME8awEqN5ffd3TyzkeOnB6QAQG3LdzVEDvr1PXuvAF"
consumer_key = "njxWAjzmYwSeytrCuFBES6xe5"
consumer_secret = "jJ07541FMr3l9QS9V5EDOOzm9O2OPdJkkBYvGlEpgR1JgpjUcM"
  
# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  
# set access to user's access key and access secret 
auth.set_access_token(access_token, access_token_secret)
  
# calling the api 
api = tweepy.API(auth)

# number max of statuses we can count
count = 200

# data using user_timeline (Tweets)
nbTweets = []
tweets_month = []
tweets_week = []
likes = []
time = []
last_tweet = []
hashtags = []
mentions = []

# data using get_user (Users)
nbFollowers = []

# list of Twitter URLs
url_list = 'twitterURL.csv'

# today's date
today = datetime.datetime.now()

# activity details
with open (url_list, 'r', encoding= 'utf-8') as file :
    readlines = file.read().splitlines()
    for line in readlines :
        user_id = line.split('/')[-1]
        f = api.get_user(user_id).followers_count
        nbFollowers.append(f)
        n = 0
        m = 0
        s = 0
        # list of data per user
        likes_user = []
        time_user = []
        hashtags_user = []        
        mentions_user = []
        for i in tweepy.Cursor(api.user_timeline, id = user_id, tweet_mode = 'extended', inculde_rts = 'false', encoding = 'utf-8').items(count):
            likes_user.append(i.favorite_count)
            time_user.append(str(i.created_at).split(' ')[0])
            if today - i.created_at < datetime.timedelta(days = 30):
                m = m + 1
                if today - i.created_at < datetime.timedelta(days = 7):
                    s = s + 1
            # content details
            for j in i.full_text.split():
                if j[0] == '@':
                    mentions_user.append(str(j[1:]))
                if j[0] == "#":
                    hashtags_user.append(str(j[1:]))
            n = n + 1
        nbTweets.append(n)
        tweets_month.append(m)
        tweets_week.append(s)
        # inject lists per user in general lists
        likes.append(likes_user)
        time.append(time_user)
        last_tweet.append(time_user[0])
        hashtags.append(hashtags_user)
        mentions.append(mentions_user)