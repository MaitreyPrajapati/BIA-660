# Read this first: https://www.w3schools.com/html/default.asp
from selenium import webdriver
import time
import csv

"""
A function that uses selenium and chromedriver to get tweets from a Twitter account.
url is the link the account
scrollNum is the number of times we want to scroll to load more tweets.
"""

def getTweets(url, scrollNum):
    #open the browser and visit the url
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(2)

    already_seen=set()#keeps track of tweets we have already seen.

    #write the tweets to a file
    fw=open('tweets.txt','w',encoding='utf8')
    writer=csv.writer(fw,lineterminator='\n')#create a csv writer for this file
    for i in range(scrollNum):

        print('batch count',i)
        
        #find all elements that have the value "tweet" for the data-testid attribute
        tweets=driver.find_elements_by_css_selector('div[data-testid="tweet"]')#
        print(len(tweets),' tweets found\n')
        
        for tweet in tweets:

            if tweet in already_seen:continue #we have seen this tweet before while scrolling down, ignore
            already_seen.add(tweet) #first time we see this tweet. Mark as seen and process.
        
            txt,retweets='NA','NA'
        
            try: 
                txt=tweet.find_element_by_css_selector("div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0").text
                txt=txt.replace('\n', ' ')
            except: 
                print ('no text')     

            try:
        
                #find the div element that havs the value "retweet" for the data-testid attribute
                retweetElement=tweet.find_element_by_css_selector('div[data-testid="retweet"]')
 
                #find the span element that has all the specified values (space separated) in its class attribute
                retweets=retweetElement.find_element_by_css_selector('span.css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0').text  
                                  
            except:
                print ('no retweets')

            #only write tweets that have text or retweets (or both). 
            if txt!='NA' or retweets!='NA':
                writer.writerow([txt,retweets])

        #scroll down twice to load more tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(2)

    fw.close()
    print('done')


url='https://twitter.com/SHAQ'
getTweets(url,5)