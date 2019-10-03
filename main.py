import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 

class TwitterClient(object): 
    def __init__(self): 
        # my keys and tokens
        consumer_key = 'QnAoQXG7bFP6fnGOuT4Sgeo23 '
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
            fetched_tweets = self.api.search(q = query, count = count) 
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
    api = TwitterClient() 
    tweets = api.get_tweets(query = 'Donald Trump', count = 200) 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    print("Neutral tweets percentage: {} % \ ".format(100*len(tweets - ntweets - ptweets)/len(tweets))) 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text'])   
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text']) 
  
if __name__ == "__main__": 
    main() 