import os
import sys
import csv
import requests
import json

from bs4 import BeautifulSoup
import newspaper

# Specify where the google search api package is (hard to install this package using sudo)
sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)), '../Google-Search-API/'))
from google import google




def get_article_from_resources(res_dir='/resources'):

    """
    no
    :return:
    """
    # Getting article pages from resources directory
    BASEPATH = os.path.dirname(os.path.abspath(__file__))
    RESOURCE_DIR_ABS = BASEPATH + res_dir

    files_location = []
    for file in os.listdir(RESOURCE_DIR_ABS):
        files_location.append(os.path.join(RESOURCE_DIR_ABS, file))

    all_urls = []
    for file in files_location:
        f = open(file, 'r')
        lines = f.readlines()
    #    num_lines = sum(1 for line in open(file))
    #    print ("number of lines for file" + file + " is " + str(num_lines))
        for line in lines:
            # if last character is \n
            if line[-1] == '\n':
                all_urls.append(line[:-1])
            else:
                all_urls.append(line)
        f.close()

    url = all_urls[0]
    test

    # cnn_paper = newspaper.build('http://cnn.com')
    # for article in cnn_paper.articles:
    #     print(article.url)
    # Library recently has some issues
    # for i, url in enumerate(all_urls):
    #     if i > 3:
    #         break
    #
    #     yellowpage = newspaper.build(url)
    #     print(len(yellowpage.articles))



def get_article_from_search_api():
    NUM_OF_PAGE = 1

    keywords = ["DST systems scandal"]

    for keyword in keywords:
        search_results = google.search(keyword, NUM_OF_PAGE)
        for i, search_result in enumerate(search_results):
            if i < 1:
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


def get_info_from_social_media():
    # TODO: This one doesn't take priority, and The data format might vary
    # Source: Twitter, LinkedIn, Glassdoor etc.
    pass


def get_article_pages():
    source1 = get_article_from_resources()
    source2 = get_article_from_search_api()


#get_article_from_resources()
#get_article_from_search_api()




