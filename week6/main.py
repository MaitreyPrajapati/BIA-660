from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
from collections import defaultdict
import time

# Loads the page, Returns as many tweets along with their counter and text(Max : 30)
# Input : link: link to twitter-user-page, _type : used for the counter, type can either be 'like' or 'comment'
# Output : dictionary in the format { selenium WebElement to the tweet : [Text of the tweet, counter(likes/comments)]
def getTweets(link, _type):
    driver = webdriver.Chrome('chromeDriver/chromedriver')
    last_height, curr_height = 0, 1
    tweet_dict = defaultdict()
    driver.get(link)

    try:
        while curr_height != last_height and len(tweet_dict) < 30:

            last_height = driver.execute_script("return document.body.scrollHeight")
            tweets = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="tweet"]')))

            if tweets:
                for t in tweets:
                    _type_counter = 0
                    tweet_text = t.find_elements_by_css_selector('span[class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"]')
                    try:
                        _type_counter = t.find_element_by_css_selector('div[data-testid="' + _type + '"]').text
                    except:
                        pass

                    if(tweet_text):
                        tweet_text = ' '.join([line.text for line in tweet_text[:-3]])
                        tweet_text = tweet_text.split('·')
                        tweet_dict[t] = [tweet_text[min(len(tweet_text)-1, 1)], _type_counter]

                        if len(tweet_dict) == 30:
                            break

            else:
                print("No tweets left", len(tweet_dict))

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            curr_height = driver.execute_script("return document.body.scrollHeight")
            time.sleep(3)

    except Exception as e:
        print("Caught an error while trying", link)
        driver.close()
    return tweet_dict

# Returns the most commented/liked tweets
# Returns : WebElement of the tweet, [Actual Tweet text, counter of likes/comments]
def getEmTweet(link, _type):
    letter_to_float = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    tweets = getTweets(link, _type)
    for i,j in tweets.items():
        text, counter = j
        if counter:
            if(counter[-1] in letter_to_float):
                tweets[i][1] = float(counter[:-1]) * letter_to_float[counter[-1]]
            else:
                tweets[i][1] = float(counter)
        else:
            tweets[i][1] = 0

    max_val = max(tweets, key= lambda x : tweets[x][1])
    return max_val, tweets[max_val]

# Returns most common words among two tweets
def getCommonWords(link1, link2):

    returnSet = set()

    tweet_one = str(getEmTweet(link1, 'reply')[1][0])
    tweet_two = str(getEmTweet(link2, 'like')[1][0])
    tweet_one = set(re.sub(r'(\n|,|\.|/\n|\\)', ' ', tweet_one).split(' '))
    tweet_two = set(re.sub(r'(\n|,|\.|/\n|\\)', ' ', tweet_two).split(' '))

    for i in tweet_one:
        if i and i in tweet_two:
            returnSet.add(i)

    return returnSet


if __name__ == '__main__':
    link1 = 'https://twitter.com/SHAQ'
    link2 = 'https://twitter.com/KingJames'
    print(getCommonWords(link1, link2))