import tweepy
import pandas as pd
from textblob import TextBlob
import re
import matplotlib.pyplot as plt

# Twitter API v2 credentials (Bearer Token)
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAKGKwQEAAAAANhI0QRKjkBopALlGBSTmpIL5gfY%3DwYoWJMkeoYAuulYEze7wmTG9xp5QExDdSwytCcWRf9IvGvkq3Y'  # Replace with your actual Bearer Token

# Tweepy client with Bearer Token authentication
client = tweepy.Client(bearer_token=bearer_token)

# Function to clean tweets
def clean_tweet(tweet):
    tweet = re.sub(r'@[A-Za-z0-9_]+', '', tweet)  # Remove mentions
    tweet = re.sub(r'#', '', tweet)  # Remove the '#' symbol
    tweet = re.sub(r'RT[\s]+', '', tweet)  # Remove retweets
    tweet = re.sub(r'https?:\/\/\S+', '', tweet)  # Remove hyperlinks
    return tweet

# Function to perform sentiment analysis
def get_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Function to collect Tweets using Twitter API v2
def get_tweets_v2(query, count=100):
    query += " -is:retweet lang:en"
    try:
        tweets = client.search_recent_tweets(query=query, max_results=count, tweet_fields=["created_at"])
        if tweets.data:
            tweet_list = [[tweet.text, tweet.created_at] for tweet in tweets.data]
            df = pd.DataFrame(tweet_list, columns=['Tweet', 'Created At'])
            df['Cleaned Tweet'] = df['Tweet'].apply(clean_tweet)
            df['Sentiment'] = df['Cleaned Tweet'].apply(get_sentiment)
            return df
        else:
            print("No tweets found for the specified query.")
            return pd.DataFrame(columns=['Tweet', 'Created At', 'Cleaned Tweet', 'Sentiment'])
    except tweepy.errors.Forbidden as e:
        print("Error: Forbidden - Check your API credentials or project permissions.")
        return pd.DataFrame(columns=['Tweet', 'Created At', 'Cleaned Tweet', 'Sentiment'])
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame(columns=['Tweet', 'Created At', 'Cleaned Tweet', 'Sentiment'])

# Example: Scraping tweets with hashtag #AAPL using Twitter API v2
df = get_tweets_v2("#AAPL", count=100)

# Save the results to a CSV file
df.to_csv('AAPL_tweets.csv', index=False)

# Print a sample of the data
print(df.head())

# Plot sentiment distribution
plt.figure(figsize=(10, 6))
plt.bar(df['Sentiment'].value_counts().index, df['Sentiment'].value_counts())
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.title('Sentiment Distribution of #AAPL Tweets')
plt.show()
