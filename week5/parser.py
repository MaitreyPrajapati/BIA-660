from bs4 import BeautifulSoup
import requests
import re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
URLEXTENSION = "?type=&sort=&page="

# Requests the page for the url and returns the output
def getPage(url):
    res = None
    for i in range(5):
        try:
            res = requests.get(url, headers=HEADERS)
        except:
            print("Try {} failed into getting the {}.".format(i, url))
        if(res): break
    return res


# Extracts critic's name and publication from the review
def extractCriticInfo(review):
    publication = None
    critic = review.find('div', {'class' : 'critic_name'}).find('a', recursive=False).contents[0]

    try: publication = review.find('div', {'class' : 'critic_name'}).find('em')
    except: pass

    publication = publication.contents[0] if publication else 'NA'
    return critic, publication


# Extracts rating of the critic, review's text and date from the review
def extractReviewInfo(review):
    rating, reviewText, date = None, None, None
    reviewContainer = review.find('div', {'class' : 'review_container'})

    try: rating = reviewContainer.find('div', {'class' : re.compile('[rotten|fresh]')})['class'][-1]
    except : rating = 'NA'

    try: reviewText = reviewContainer.find('div', {'class' : 'the_review'}).contents[0].strip()
    except: reviewText = 'NA'

    try: date = reviewContainer.find('div', {'class' : 'review-date'}).contents[0].strip()
    except : date = 'NA'

    return rating, reviewText, date


# Load page html in bs4 and loads reviews into file
def loadReviewsInFile(soup, outputFilePath):
    reviews= soup.find('div', {'class' : 'review_table'}).find_all('div', {'class' : 'row review_table_row'})
    with open(outputFilePath, 'a') as file:
        for review in reviews:
            critic, publication = extractCriticInfo(review)
            rating, reviewText, date = extractReviewInfo(review)
            file.write(','.join([critic, rating, publication, reviewText, date]))
            file.write('\n')


def run(movieUrl):
    outputFilePath = 'output.txt'

    # For the first page
    url = getPage(movieUrl)
    if not url: return "Can not load the url that is given."
    soup = BeautifulSoup(url.text, 'html.parser')
    loadReviewsInFile(soup, outputFilePath)

    # For the second page
    secondPageUrl = getPage(movieUrl + URLEXTENSION + str(2))
    if not url: return "Can not load second page"
    secondSoup = BeautifulSoup(secondPageUrl.text, 'html.parser')
    loadReviewsInFile(secondSoup, outputFilePath)

    return


if __name__ == '__main__':
    link = 'https://www.rottentomatoes.com/m/enola_holmes/reviews'
    run(link)


