from newspaper import Article
#
# url = 'https://www.irishtimes.com/'
# article = Article(url)
# article.download()
# article.parse()

import newspaper

RELATED_KEYWORDS = ['DST', 'BFDS', 'Argus', 'Kasina', 'Steve Hooley']
RELATED_KEYWORDS = [x.lower() for x in RELATED_KEYWORDS]

NEGATIVE_KEYWORDS = ['Scandal', 'Layoff', 'Terrible']
NEGATIVE_KEYWORDS = [x.lower() for x in NEGATIVE_KEYWORDS]
# TODO: positive words
# POSITIVE_KEYWORDS = []

#
potential_articles = []
negative_articles = []


# NOTE: Single newspaper test
# This part is multi-threading
bloomberg_paper = newspaper.build('http://www.cnn.com')

# count = 0
# for article in bloomberg_paper.articles:
#     article.build()
#     print("##############")
#     print(article.keywords)
#     print(article.summary)
#     print("##############")
#     count += 1
#     if count == 3:
#         break


for article in bloomberg_paper.articles:
    try:
        article.build()  # Contains download, parse and nlp
    except:
        print("Article Exception has been caught")
        continue

    print("Article keywords are: ")
    print(article.keywords)

    for related_keyword in RELATED_KEYWORDS:
        if related_keyword in article.text.lower():
            potential_articles.append(article)

            for negative_keyword in NEGATIVE_KEYWORDS:
                if negative_keyword in article.text.lower():
                    negative_articles.append(article)
                break  # Break negative keyword, so for article contains multiple keywords won't be duplicated

            break  # Break related keyword, so for article contains multiple keywords won't be duplicated


print("We have %s potential articles" % len(potential_articles))
print("We have %s negative articles" % len(negative_articles))


    # print(article.url)