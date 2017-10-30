import tweepy
import sys
import time
import json


# TODO: Change some print to loggings
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, save_as_file, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.saveFile = open(save_as_file, 'w')
        super(MyStreamListener, self).__init__()

    def on_data(self, tweet):
        """
        Write to file or write to db
        :param tweet: a tweet object
        :return: None
        """
        if (time.time() - self.start_time) < self.limit:
            self.saveFile.write(tweet)
            return True
        else:
            self.saveFile.close()
            return False

    def on_status(self, tweet):
        if (time.time() - self.start_time) >= self.limit:
            print('time is over')
            return False

    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True  # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True  # Don't kill the stream


class Tweet(object):
    def __init__(self, topics=None, tweet_file=None, mode='batch'):
        """
        Authenticate, define interested topics to search, define running mode
        :param topics: str[]
        :param tweet_file: where the tweet file is located
        :param mode: str ('batch' or 'stream')
        """
        self.topics = topics
        self.GEN_MAX_TWEET = 100  # the max number of tweets to generate(The twitter API will only return a max of 100 count)
        self.tweet_file = tweet_file
        self.mode = mode
        self.tweets = []

        if topics and tweet_file:
            print("WARNING! you input both topics and the tweet file, only one is expected")
            exit(-1)

        if not topics and not tweet_file:
            print("WARNING! you input either topics or tweet file, one is expected")
            exit(-1)

        # If file argument is given, it will not connect to twitter server
        # It will just save tweets in self.tweets
        if tweet_file:
            with open(tweet_file, 'r') as infile:
                for line in infile:
                    self.tweets.append(json.loads(line))

        else:
            consumer_key = 'bbqKfXEU2VJNoWlYJvbdtptOE'
            consumer_secret = 'afPk2JuMMMD6IhP5Xijo60ni4FUK39PDzhU7ylgT9FgNZX9ngh'
            access_token = '434708489-DTeHfK4OYKRuIXlfoWnNgzzwpEZTPCEpSMv8C0ll'
            access_token_secret = 'SjWFYfX2k3q4RJKQXcP1LP9ikhRfckPKOEcrb2cpQ0A0n'

            # Attempt authentication
            try:
                # create OAuthHandler object
                self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                # set access token and secret
                self.auth.set_access_token(access_token, access_token_secret)
                # create tweepy API object to fetch tweets
                self.api = tweepy.API(self.auth)
            except:
                print("Error: Authentication Failed")
                exit(-1)

    def gen_tweets(self, save_as_tweet_file='tweet_file.txt', save_file=True, time_limit=60):
        """
        Generate the tweet
        :param save_as_tweet_file: <str> file will be saved as this name
        :param save_file: <bool> Are we gonna save the tweet in a file?
        :param time_limit: <int> For streaming mode only, # of seconds to listen to stream
        :return:
        """
        if self.tweet_file:
            print("INFO: You have given a tweet file, you don't need to generate tweets!")
            return None

        # batch mode generating the tweets
        if self.mode == 'batch':
            # search_results = api.search(q=['#argus', '#dstsystems', '#BFDS'], lang='en', count=100)
            self.tweets = self.api.search(q=self.topics, count=self.GEN_MAX_TWEET)
            if not save_file:
                return self.tweets
            else:
                with open(save_as_tweet_file, 'w') as outfile:
                    for tweet in self.tweets:
                        # json.dump(tweet._json, outfile, sort_keys=True, indent=4)
                        json.dump(tweet._json, outfile, sort_keys=True)
                        outfile.write('\n')

        # stream mode generating the tweets
        elif self.mode == 'stream':
            tweet_stream_listener = MyStreamListener(save_as_file=save_as_tweet_file, time_limit=time_limit)
            tweet_stream = tweepy.Stream(auth=self.api.auth, listener=tweet_stream_listener)
            # Don't set language, or there's no stream data, maybe because language='en' it's not the correct value
            tweet_stream.filter(track=self.topics, async=True)

    def get_tweets(self):
        if self.tweet_file:  # Read tweet from file, implemented in __init__ function
            return self.tweets
        else:  # Read tweet by topic, need to generate tweet first, only 'batch' mode is supported
            if self.mode == 'batch':
                return self.gen_tweets(save_file=False)  # Don't save the searched tweet as a file
            else:
                print("WARNING! You're trying to get real time tweet "
                      "and use it as an python object, not supported now. "
                      "You can generate stream data first and save it in files or database "
                      "and then read from it")
                exit(-1)


def limit_handled(cursor):
    # TODO: possibly need this function to limit request frequency
    """ Limit the request sent to twitter server"""
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(60)


