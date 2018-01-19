import os
import requests
import json
from bs4 import BeautifulSoup
from google import google

os.chdir(os.path.dirname(os.path.abspath(__file__)))

NUM_OF_PAGE = 1

keywords = ["DST systems scandal"]

for keyword in keywords:
    search_results = google.search(keyword, NUM_OF_PAGE)
    for i, search_result in enumerate(search_results):
        if i<1:
            response = requests.get(search_result.link)
            soup = BeautifulSoup(response.text, 'lxml')
            print(soup.body.prettify())
        # print("The " + str(i) + " result")
        # print("######")
        # print (search_result.name)
        # print (search_result.description)
        # print (search_result.link)
        # print (search_result.google_link)
        # print ("#####")
