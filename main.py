import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import spacy as sp

class TwitterClient(object): 
    def __init__(self): 
        # my keys and tokens
        """consumer_key = "XXXXXXXXXXXXXXXXXXXXXXX"
                                consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                                access_token =    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                                access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'"""
        
        consumer_key = 'f0WxE7bB3uQwOle3zJcWmJJVD'
        consumer_secret = 'w64Q2GKzeE1zHSUw4OcnXyufNiYDMzHmEj1oeUz0YQxZj9w13U'
        access_token =    '354821837-TUMg1Wycx5ZED2IAQqGMJnTx8XbfOPiPln61Fogf'
        access_token_secret = 'ZmPIvKxWncWRQnLmuUeg0xqfCAndwyTHNjzojP3FBPKio'
  
        self.authorization = OAuthHandler(consumer_key, consumer_secret) 
        self.authorization.set_access_token(access_token, access_token_secret) 
        self.api = tweepy.API(self.authorization) 
    
    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, geocode, count = 10): 
        tweets = [] 
        try: 
            #fetched_tweets = self.api.search(q = query,lang=lang,geocode=geocode,count = count) 
            fetched_tweets = self.api.search(q = query, geocode = geocode, count = count) 
            for tweet in fetched_tweets: 
                parsed_tweet = {} 
                parsed_tweet['text'] = tweet.text 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
            return tweets 
        except tweepy.TweepError as e: 
            print("Error : " + str(e)) 
def main():
    while(True):
        print("Starting TwitterClient")
        api = TwitterClient() 
        query = input("Enter your intrest: ")
        km = 10000
        geoc = {'india':(22.3511148,78.6677428,km), 'USA':(39.7837304, 39.7837304, km), 'Russia':(64.6863136, 97.7453061,km)}
        geocode = input("Enter location preference(1:India, 2:USA, 3:Russia):")
        if(geocode==''):
            geocode = ""
        else:
            geocode=geoc[list(geoc.keys())[int(geocode)-1]]

        tweets = api.get_tweets(query, geocode = geocode, count = 100)
        if(len(tweets)==0):
            print("No result for the search! Try again")
            continue

        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
        print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 
        print("\n\nPositive tweets:") 
        for tweet in ptweets[:5]: 
            print(tweet['text'][:25])   
        print("\n\nNegative tweets:") 
        for tweet in ntweets[:5]: 
            print(tweet['text'][:25]) 
        break
if __name__ == "__main__": 
    main() 