import os
import sys
import logging
import requests
import json
from newspaper import fulltext
from bs4 import BeautifulSoup
from sqlalchemy import exists

from model import *

# Specify where the google search api package is (hard to install this package using sudo)
sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)), '../Google-Search-API/'))
from google import google

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s')

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

                new_article = RelatedArticles(search_result.link, soup.title.contents, keyword, txt)
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


            # print("The " + str(i) + " result")
            # print("######")
            # print (search_result.name)
            # print (search_result.description)
            # print (search_result.link)
            # print (search_result.google_link)
            # print ("#####")
