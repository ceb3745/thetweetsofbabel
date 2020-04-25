# The Tweets of Babel
# By: Julie, Morgan, Carson
#

import jsonpickle as jsonpickle
from twython import Twython
import tweepy
import random
import requests
import os
import re
import time


# Twitter application authentication
# You get these credentials by registering your app with Twitter
# #test account
#CONSUMER API KEY & SECRET
API_KEY  = ''
API_SECRET = ''
#ACCESS TOKEN & SECRET
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''


words = ['here', 'is', 'a', 'penguin', 'boi', 'with', 'an', 'orange', 'so', 'you', 'can', 'learn', 'more', 'and', 'id', 'have', 'gotten', 'away', 'it,', 'too,', 'if', 'it', 'werent', 'for', 'those', 'meddling', 'kids', 'how', 'are', 'doing', 'let', 'us', 'try', 'this', 'again', 'cat', 'soft', 'round', 'what', 'do', 'think', 'of', 'my', 'photography', 'read', 'the', 'library', 'babel', 'thanks', 'responding', 'take', 'your', 'time', 'pigeon', 'love', 'i', 'pigeons', 'yay', 'pigeoning', 'hey', 'there', 'were', 'some', 'real', 'words', 'in', 'that', 'boy', 'every', 'tweet', 'will', 'append', 'these', 'to', 'dictionary', 'eat', 'tiny', 'dog', 'now', 'toilet', 'paper', 'tomato', 'soup', 'necessities', 'seen', 'kingdom', 'on', 'netflix', 'good', 'baby', 'pinecones', 'balcony', 'pretty.', 'would', 'like', 'live', 'today', 'bro', 'awake', 'kinds', 'shows', 'who', 'when', 'where', 'why', 'life', 'gives', 'beef,', 'make', 'hamburger', 'look', 'at', 'scarf', 'made', 'his', 'name', 'peanut', 'feel', 'about', 'snow', 'april']
def getWord():
    num = random.randint(0, len(words) - 1)
    return words[num]

def gibberish():
    if words:
        print(words)
        arr = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
               "v", "w", "x", "y", "z", " ", ".", ",", "word", "word", "word", "word", "word", "word", "word", "word", "word", "word", "word", "word"]
    else:
        arr = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
               "v",
               "w", "x", "y", "z", " ", ".", ","]

    num = random.randint(2, 60)
    stringResult = ""

    for x in range(0, num):
        index = random.randint(0, len(arr) - 1)
        if arr[index] == "word":
            stringResult = stringResult + " " + getWord() + " "
        else:
            stringResult = stringResult + arr[index]

    print(stringResult)
    return stringResult

def fix_message(str):
    #add words

    arr = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ".", ","]

    lowerCase = str.lower()
    chars = list(map(lambda i: i, lowerCase))
    print(chars)
    for char in chars:
        if char not in arr:
            chars[chars.index(char)] = ""

    finalMsg = ""
    finalMsg = finalMsg.join(chars)
    print(finalMsg)

    newWords = (finalMsg + " ").split()
    for word in newWords:
        if word not in words:
            words.append(word)

    print(words)

    return finalMsg + " "


def tweet_image(api, url, message):
    filename = 'temp.jpg'
    print(url)
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=message, in_reply_to_status_id=tweetJson.get("id"))
        #os.remove(filename)
    else:
        print("Unable to download image")

tweetIds = []

while(True):
    # connect to the TWitter API using your app's credentials
    twythonAPI = Twython(API_KEY, API_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    # api.update_status(status= "Why would cheap bots done quick do this to us!")

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    tweepyAPI = tweepy.API(auth)

    max_id = -1
    count = 0;

    maxTweets = 1

    tweetCount = 0
    fName = 'tweets.txt'
    searchQuery = '@CryptoldeaTest'
    retweet_filter = '-filter:retweets'
    q = searchQuery + retweet_filter
    tweetsPerQry = 2
    sinceId = None
    flagNoTweets = True

    print("Downloading max {0} tweets".format(maxTweets))
    with open(fName, 'w') as f:
        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = tweepyAPI.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended')
                    else:
                        new_tweets = tweepyAPI.search(q=searchQuery, count=tweetsPerQry,
                                                since_id=sinceId, tweet_mode='extended')
                else:
                    if (not sinceId):
                        new_tweets = tweepyAPI.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1), tweet_mode='extended')
                    else:
                        new_tweets = tweepyAPI.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId, tweet_mode='extended')
                if not new_tweets:
                    print("No more tweets found")
                    break

                for tweet in new_tweets:
                    flag = False

                    tweetJson = tweet._json
                    checkReplies = tweepyAPI.search(q="@"+tweetJson.get("user").get("screen_name") +  ' -filter:retweets from:CryptoLdeaTest', count=tweetsPerQry,
                                                  max_id=str(max_id - 1),
                                                  since_id=None, tweet_mode='extended')
                    for reply in checkReplies:
                        replyJson = reply._json
                        message = tweetJson.get("full_text").replace("@CryptoldeaTest", "")

                        if 'https' in message:
                            indexOfHttps = message.index('https')
                            message = fix_message(message[:indexOfHttps])
                        else:
                            message = fix_message(message)

                        print(replyJson)

                        if replyJson.get("in_reply_to_status_id") == tweetJson.get("id"):
                            print("REPLY FOUND")
                            flag = True

                    if not flag:
                        flagNoTweets = False
                        print(tweetJson.get("full_text"))
                        print(tweetJson)
                        print(tweetJson.get("user").get("screen_name"))
                        message = tweetJson.get("full_text").replace("@CryptoldeaTest", "")

                        if 'https' in message:
                            indexOfHttps = message.index('https')
                            message = fix_message(message[:indexOfHttps])
                        else:
                            message = fix_message(message)

                        message = gibberish() + message + gibberish()

                        userString = " @" + tweetJson.get("user").get("screen_name")
                        message = message + userString
                        if (tweetJson.get("entities").get("media") != None):
                            tweet_image(tweepyAPI, tweetJson.get("entities").get("media")[0].get("media_url_https"),
                                        message)
                        else:
                            twythonAPI.update_status(status=message, in_reply_to_status_id=tweetJson.get("id"))
                        tweetIds.append(tweetJson.get("id"))


                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
    count = count+1
    if(count % 10 == 0):
        if flagNoTweets:
            message = gibberish() + gibberish()
            twythonAPI.update_status(status=message)
            words.append("word")

    flagNoTweets = True
    time.sleep(120)

