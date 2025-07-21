import tweepy
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Authenticate with Twitter API v2 ---
def get_twitter_client():
    """Sets up and returns a Tweepy client for Twitter API v2."""
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    print("Authentication with Twitter successful.")
    return client

# --- Core Logic ---
def post_next_tweet(csv_file='tweets.csv'):
    """Finds the next unposted tweet, posts it, and updates the CSV."""
    # 1. Read the tweet schedule
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
        return

    # 2. Find the next tweet that has not been posted
    unposted_tweets = df[df['posted_status'] == 'no']
    
    if unposted_tweets.empty:
        print("🎉 Challenge complete! All tweets have been posted.")
        return

    # Get the first unposted tweet
    next_tweet_series = unposted_tweets.iloc[0]
    tweet_text = next_tweet_series['tweet_text']
    tweet_index = next_tweet_series.name # This is the original index in the dataframe

    print(f"Found next tweet to post (Day {next_tweet_series['day']}):\n'{tweet_text}'")

    # 3. Post the tweet
    try:
        client = get_twitter_client()
        response = client.create_tweet(text=tweet_text)
        print(f"Tweet successfully posted! Tweet ID: {response.data['id']}")

        # 4. Update the CSV file to mark the tweet as posted
        df.loc[tweet_index, 'posted_status'] = 'yes'
        df.to_csv(csv_file, index=False)
        print(f"Updated {csv_file} to mark Day {next_tweet_series['day']} as 'yes'.")

    except Exception as e:
        print(f"An error occurred while posting the tweet: {e}")

# --- Run the script ---
if __name__ == "__main__":
    post_next_tweet()