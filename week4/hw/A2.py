import re
import requests
from nltk.corpus import stopwords
from collections import defaultdict

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

# Loading stopWords
def loadStopWords():
    return stopwords.words('english')

# input : link
# output : text from the response
def loadLink(url):
    return_obj = None
    for i in range(5):
        try:
            return_obj = requests.get(url, headers=HEADERS).text
        except:
            print("Try {} : {} not loaded.".format(i, url))
    return return_obj

# input : text
# output : splitted words that are isalpha()
def splitWords(text):
    return re.sub('[^a-z]', ' ', text.lower()).split(' ')

# input : Dictionary, splitted words, stopwords
# output : Loaded dictionary made up of splitted words omitting words from stopwords
def loadWordsInDict(counter, words, stopLex):
    for w in words:
        if w and w not in stopLex:
            counter[w] += 1
    return counter

def run(link1, link2, link3):
    l1, l2, l3 = loadLink(link1), loadLink(link2), loadLink(link3)
    if not l1 or not l2 or not l3:
        return "One or more of the three links failed to load"

    return_set = set()
    stop_lex = loadStopWords()

    l1, l2, l3 = splitWords(l1), splitWords(l2), splitWords(l3)

    d1 = loadWordsInDict(defaultdict(int), l1, stop_lex)
    d2 = loadWordsInDict(defaultdict(int), l2, stop_lex)
    d3 = loadWordsInDict(defaultdict(int), l3, stop_lex)

    for key, val in d2.items():
        if d1[key] < val < d3[key]:
            return_set.add(key)

    return return_set

if __name__ == '__main__':
    link1 = 'https://twitter.com/robots.txt'
    link2 = 'https://www.glassdoor.com/robots.txt'
    link3 = 'https://www.facebook.com/robots.txt'
    print(run(link1, link2, link3))
