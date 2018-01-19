"""
Get the twitter data, batch or real time, store in the csv file or database
"""
import tweepy
import logging
import argparse
from tweet import Tweet


parser = argparse.ArgumentParser()
parser.add_argument(
        '-v', '--verbose'
        , help='print status information'
        , action='store_const', dest='log_level', const=logging.INFO
        , default=logging.WARNING)
parser.add_argument(
        '-d', '--debug'
        , help='print debugging information'
        , action='store_const', dest='log_level', const=logging.DEBUG)
parser.add_argument(
    '-m', '--mode',
    choices=['batch', 'stream'],
    help='Specify the mode to generate twitter data, batch or stream, default is batch',
    default='batch'
)
parser.add_argument(
    '-s', '--save',
    choices=['csv', 'db'],
    help='Specify the mode to save twitter data, save in csv or db(database), default is db',
    default='db'
)
args = parser.parse_args()
logging.basicConfig(
        level=args.log_level,
        format='%(asctime)s %(levelname)-8s %(message)s'
)

###################################################
#             Setup interested topics             #
###################################################
my_topics = ['trump']


#################################
#             batch             #
#################################
if args.mode == 'batch':
    # Tweet(topics=my_topics, mode=args.mode).gen_tweets()
    my_tweets = Tweet(topics=my_topics, mode=args.mode).get_tweets()
    print(len(my_tweets))


#################################
#             stream            #
#################################
if args.mode == 'stream':
    pass


# Get tweets that has the information we're interested in
# Find out when it was tweeted, who tweeted it, and how many followers he has

