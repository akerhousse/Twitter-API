import tweepy
import csv
import datetime
import json
import itertools
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

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

url_list = 'twitterURL.csv'

# data using user_timeline (Tweets)
count = 5
users = []
nbtweets = []
active = []
tweets_month = []
tweets_week = []
likes_total = []
#likes_tweet = []
time = []
last_tweet = []
hashtags = []
mentions = []
nbfollowers = []
today = datetime.datetime.now()

# open and read csv file
with open (url_list, 'r', encoding= 'utf-8-sig') as file :
    readlines = file.read().splitlines()
    # loop on accounts
    for line in readlines :
        user_id = line.split('/')[-1]
        users.append({"i":user_id,"u":line})   
        f = api.get_user(user_id).followers_count
        nbfollowers.append(f)
        n = 0 # total number of tweets
        m = 0 # number of tweets per month
        s = 0 # number of tweets per week
        l = 0 # total number of likes
        # list of data per user
        likes_user = []
        time_user = []
        hashtags_user = []        
        mentions_user = []
        a = False
        # loop of tweet from the current account
        for i in tweepy.Cursor(api.user_timeline, id = user_id, tweet_mode = 'extended', inculde_rts = 'false', encoding = 'utf-8-sig').items(count):
            likes_user.append(i.favorite_count)
            l = l + i.favorite_count
            time_user.append(str(i.created_at).split(' ')[0])
            if today - i.created_at < datetime.timedelta(days = 30):
                m = m + 1
                if today - i.created_at < datetime.timedelta(days = 7):
                    s = s + 1
                    a = True
            # content details
            for j in i.full_text.split():
                if j[0] == '@':
                    mentions_user.append(str(j[1:]))
                if j[0] == '#':
                    hashtags_user.append(str(j[1:]))
            n = n + 1
        nbtweets.append(n)
        tweets_month.append(m)
        tweets_week.append(s)
        likes_total.append(l)
        # inject lists per user in general lists
        #likes_tweet.append(likes_user)
        time.append(time_user)
        last_tweet.append(time_user[0])
        hashtags.append(hashtags_user)
        mentions.append(mentions_user)
        if a:
            active.append({"i":user_id,"n":s,"u":line})

def get_n(active):
    return active.get("n")

active.sort(key=get_n,reverse=True)

top_3 = active[0:3]
top_6 = active[3:6]
 
def cal_average(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t           
    avg = sum_num / len(num)
    return round(avg)

tweets_avg = cal_average(nbtweets)
followers_avg = cal_average(nbfollowers)
sum_tweets = sum(nbtweets)
max_tweets = len(users)*count
max_followers = max(nbfollowers)

numbers =  [str(followers_avg),str(sum_tweets),str(max_tweets),str(max_followers),str(count)]

with open("test.csv", "w", newline='', encoding='utf-8-sig') as outfile:
    writer = csv.writer(outfile, delimiter =',')
    writer.writerow(str(i) for i in top_3)
    writer.writerow(str(i) for i in top_6)
    writer.writerow(str(i) for i in users)
    writer.writerow(str(i) for i in nbfollowers)
    writer.writerow(str(i) for i in nbtweets)
    writer.writerow(str(i) for i in likes_total)
    writer.writerow(str(i) for i in last_tweet)
    writer.writerow(str(i) for i in tweets_month)
    writer.writerow(str(i) for i in tweets_week)
    writer.writerow(str(i) for i in hashtags)
    writer.writerow(str(i) for i in mentions)
    for x in numbers:
        writer.writerow(x.split(sep=','))


with open('test.csv','r',encoding='utf-8-sig') as file:
    reader = csv.reader(file, delimiter=',')
    rows = list(reader)
    top3 = []
    top6 = []
    r_users = []
    r_nbfollowers = []
    r_nbtweets = []
    r_likes_total = []
    r_last_tweet = []
    r_tweets_month = []
    r_tweets_week = []
    r_hashtags = []
    r_mentions = []

    for i in rows[0]:
        top3.append(json.loads(i.replace("'",'"')))
    for i in rows[1]:
        top6.append(json.loads(i.replace("'",'"')))
    for i in rows[2]:
        r_users.append(json.loads(i.replace("'",'"')))
    for i in str(rows[3]):
        r_nbfollowers.append(i)
    for i in str(rows[4]):
        r_nbtweets.append(i)
    for i in str(rows[5]):
        r_likes_total.append(i)
    for i in str(rows[6]):
        r_last_tweet.append(i)
    for i in str(rows[7]):
        r_tweets_month.append(i)
    for i in str(rows[8]):
        r_tweets_week.append(i)
    for i in str(rows[9]):
        r_hashtags.append(i)
    for i in str(rows[10]):
        r_mentions.append(i)
    followers_avg = str(rows[11]).strip("[]'\'")
    sum_tweets = str(rows[12]).strip("[]'\'")
    max_tweets = str(rows[13]).strip("[]'\'")
    max_followers = str(rows[14]).strip("[]'\'")
    count = str(rows[15]).strip("[]'\'")

    ziplist = zip(r_users,r_nbfollowers,r_nbtweets,r_likes_total,r_last_tweet,r_tweets_month,r_tweets_week)
    ziplist2 = zip(r_users,r_hashtags,r_mentions)


text = ''
for i in r_hashtags:
    for j in i:
        text = text + str(j).strip("[],'\'")

custom_mask = np.array(Image.open("twitter.jpg"))
wc = WordCloud(mask = custom_mask, contour_width = 1, contour_color='steelblue', mode='RGBA', background_color='none')
wc.generate(text)
wc.to_file('output.png')
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()

#print(top3)
#print(nbFollowers)
#print(nbTweets)
#print(id_nbtweets)
#print(tweets_month)
#print(tweets_week)
#print(time)
#print(last_tweet)
#print(likes)

#print(mentions)

#print(id_active)
#print(users)