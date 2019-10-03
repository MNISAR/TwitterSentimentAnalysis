import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import spacy as sp

class TwitterClient(object): 
    def __init__(self): 
        # my keys and tokens
        consumer_key = 'QnAoQXG7bFP6fnGOuT4Sgeo23'
        consumer_secret = 'IaWEvpTFsBa2kpIbeeM8UtlNYhByreCS66j2hzWEHYsrOozcRp'
        access_token = '354821837-stouXrKg1eOpngesfU7Gm9TMch3z1qS7PejW1hdH'
        access_token_secret = '9MzzNz3PzndB4THfwVdqRyuJfdjc70KJkQbaaZhfP81Aq'
  
        try: 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret) 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Authentication Failed") 
  
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
  
    def get_tweets(self, query, count = 10): 
        tweets = [] 
        try: 
            #fetched_tweets = self.api.search(q = query,lang=lang,geocode=geocode,count = count) 
            fetched_tweets = self.api.search(q = query,count = count) 
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
        km = 1000
        geoc = {'india':(22.3511148,78.6677428,km), 'USA':(39.7837304, 39.7837304, km), 'Russia':(64.6863136, 97.7453061,km)}
        geocode = input("Enter location preference(1:India, 2:USA, 3:Russia):")
        if(geocode==''):
            geocode = geoc[list(geoc.keys())[0]]
        geocode=geoc[list(geoc.keys())[int(geocode)-1]]

        tweets = api.get_tweets(query, count = 100)
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