import os
import sys
import logging
import requests
from newspaper import fulltext
from bs4 import BeautifulSoup
from sqlalchemy import exists
import math
import yaml
from textblob import TextBlob

#################################################
#              Import local packages            #
#################################################
base_path = os.path.dirname(os.path.abspath(__file__))

try:
    sys.path.insert(0, os.path.join(base_path, '../app'))
    from model import *
except ModuleNotFoundError:
    logging.error("are you sure the model file is put at the right place?")
    sys.exit(1)

try:
    # Specify where the google search api package is (hard to install this package using sudo)
    sys.path.insert(0, os.path.join(base_path, '../../../resources/Google-Search-API/'))
    from google import google
except ModuleNotFoundError:
    logging.error("are you sure the google search api directory is at the right place?")
    sys.exit(1)

#################################################
#     Load local keyword boosting dictionary    #
#################################################
try:
    boost_dic_file = open(os.path.join(base_path, '../../../resources/keyword_boost.yaml'), 'r')
    boost_dic = yaml.load(boost_dic_file)
    boost_dic_file.close()
except FileNotFoundError:
    logging.error("are you sure keyword_boost.yaml file is at the right place?")
    sys.exit(1)


#################################################
#                Define functions               #
#################################################
def compute_related_probability(full_text):
    """
    Calculating the probability how likely the full_text is considered a negative news about a company
    :param full_text: string
    :return: probability: float
    """

    global boost_dic
    sentiment_coefficient_norm = 1
    score = 0

    full_text = full_text.lower()
    boost_sec_keywords = boost_dic['boost_keyword']
    unboost_sec_keywords = boost_dic['unboost_keywords']

    # If the same word appears in the full_text more than once, we only calculate the score once
    # Part 1: see if keywords are in the full_text to calculate the score
    # TODO: apply KMP algo here
    for word in full_text.split(' '):
        if word in boost_sec_keywords:
            score += boost_sec_keywords[word]

        if word in unboost_sec_keywords:
            score += unboost_sec_keywords[word]

    # Part 2: tweak the score by sentiment of the text
    # Since we're interested in negative news, the more negative, the higher the score
    score += -1 * sentiment_coefficient_norm * TextBlob(full_text).sentiment.polarity

    # Apply Sigmoid function
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))
    probability = sigmoid(score)
    return probability


# Setup log configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s')

# Setup connections with db
Session = sqlalchemy.orm.sessionmaker()
engine = sqlalchemy.create_engine('postgresql://localhost:5432', echo=False)
Session.configure(bind=engine)
session = Session()

NUM_OF_PAGE = 1

# TODO: Get a list of maybe 10 words, limit the search result to one page
keywords = ["Argus scandal", "DST scandal", "BFDS scandal", "DST layoff"]

#
for keyword in keywords:
    search_results = google.search(keyword, NUM_OF_PAGE)
    for i, search_result in enumerate(search_results):
        if i < 5:
            # TODO: add user agent
            try:
                response = requests.get(search_result.link)
                soup = BeautifulSoup(response.text, 'lxml')

            # fulltext function included css selector and will remove paragraph if bad words were included
                txt = fulltext(response.text)
                # if soup.title and soup.title.contents:
                #     print(search_result.link)
                #     print("title of the link is: ")
                #     print(soup.title.contents[0])
                # print(txt)

                # Compute related_probablity
                prob = compute_related_probability(txt)
                new_article = RelatedArticles(search_result.link, soup.title.contents, keyword, txt, prob)
                # Check if the new article has already saved in database
                if session.query(exists().where(RelatedArticles.link == search_result.link)).scalar():
                    logging.info("Link " + search_result.link + " is already in the database")
                    continue
                else:
                    session.add(new_article)
                    session.commit()
                    logging.info("Added a new article " + search_result.link + " to database!")
                # TODO: add logging here later
            except: # Attribute exception, OSError, Proxy exception
                continue

            print("#######################")
            # a = soup.find_all('p')
            # for each_p in a:
            #     if each_p.contents:
            #         print(each_p.contents[0])
        else:
            break



