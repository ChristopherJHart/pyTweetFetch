"""
This module is the driver for the pyTweetFetch program.

TO-DO:
    - Allow filtering of tweets via shell command

"""

import os
import sys
import tweepy
import csv

def authenticate_twitter():
    try:
        cwd = os.getcwd()
        auth_file = cwd + "\\auth.txt"

        if not os.path.isfile(auth_file):
            new_auth_file = open(auth_file, "w+")
            print "An authentication file does not exist."
            print "You will need to enter authentication information manually."
            print "Retrieve this information from apps.twitter.com"
            wr_con_key = raw_input("Enter consumer key: ")
            wr_con_sec = raw_input("Enter consumer secret: ")
            wr_acc_key = raw_input("Enter access key: ")
            wr_acc_sec = raw_input("Enter access secret: ")
            new_auth_file.write(wr_con_key + "\n")
            new_auth_file.write(wr_con_sec + "\n")
            new_auth_file.write(wr_acc_key + "\n")
            new_auth_file.write(wr_acc_sec + "\n")
            new_auth_file.close()
            print "Information written to %s." % auth_file
            print "It will be re-used the next time you use this script."

        with open(auth_file) as fp:
            auth_bulk = fp.read()

        auth_arr = auth_bulk.splitlines()
        con_key = auth_arr[0].strip()
        con_sec = auth_arr[1].strip()
        acc_key = auth_arr[2].strip()
        acc_sec = auth_arr[3].strip()

        auth = tweepy.OAuthHandler(con_key, con_sec)
        auth.set_access_token(acc_key, acc_sec)
        api = tweepy.API(auth)

        print "Twitter Authenticated"
        return api
    except IOError:
        print "[ERROR] Authentication file does not exist, and we were unable to create one!"
        sys.exit()

def get_tweets(account, num, api):
    total_tweets = []
    while len(total_tweets) < num:
        if len(total_tweets) is 0:
            tweets = api.user_timeline(screen_name=account, count=200)
            tweet_max_id = tweets[199].id
        else:
            tweets = api.user_timeline(screen_name=account, count=200, max_id=tweet_max_id)
        total_tweets = total_tweets + tweets
    tweets_set = set(total_tweets)
    return total_tweets

def write_to_csv(tweet_array, csv_file):
    if not os.path.isfile(csv_file):
        open(csv_file, 'a').close()
    with open(csv_file, "wb") as csvf:
        csv_wr = csv.writer(csvf)
        csv_wr.writerow(["Date", "Text", "URL"])
        for tweet in tweet_array:
            date = tweet.created_at
            unsan_text = tweet.text.encode("utf-8")
            url_prelim = tweet.entities["urls"]
            if url_prelim:
                url = url_prelim[0]["expanded_url"]
                text_url = url_prelim[0]["url"].encode("utf-8")
                text = unsan_text.replace(text_url, "")
            else:
                continue
            #url = tweet.entities["urls"][0]["expanded_url"]
            csv_wr.writerow([date, text, url])

def main():
    """
    ISSUES:
        - Allow parameters to be passed from command line
    """

    twitter_account = "BlueSteps"
    num_tweets = 20000
    csv_file = ""

    tweepy_api = authenticate_twitter()
    all_tweets_array = get_tweets(twitter_account, num_tweets, tweepy_api)

    if not csv_file:
        cwd = os.getcwd()
        csv_file = cwd + "\\Tweet Results.csv"
    write_to_csv(all_tweets_array, csv_file)

if __name__ == "__main__":
    main()
