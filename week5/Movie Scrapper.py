from bs4 import BeautifulSoup
import re 
import time 
import requests
import csv

def Scrapper(url):

    file_1 = open('reviews2.txt','w',encoding='utf8')
    csv_review = csv.writer(file_1,lineterminator='\n')
   
    for p in range(1,3):
        print("You are Scrapping the pageNumber:",p)
        html = None 

        link = url+'?type=&sort=&page='+str(p)

        for i in range(2):
            responses = requests.get(link,headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            if responses:
                break
            else:
                time.sleep(5)
        
        if not responses:return None

        html=responses.text# read in the text from the file
        
        soup = BeautifulSoup(html,'lxml') # parse the html 

        reviews=soup.findAll('div', {'class':'row review_table_row'}) # get all the review divs

        for review in reviews:

            critic,rating,source,text,date='NA','NA','NA','NA','NA' # initialize critic and text 
            criticChunk=review.find('a',{'href':re.compile('/critic/')})
            if criticChunk: critic=criticChunk.text.strip()

            #print(review.find('div',{'class':re.compile('^review_icon')}))
        
            if review.find('div',{'class': "review_icon icon small fresh"}): 
                rating = 'fresh'
            elif review.find('div',{'class': "review_icon icon small rotten"}): 
                rating = 'rotten'

            sourceChunk = review.find('em',{'class':re.compile('subtle critic-publication')})
            if sourceChunk: source = sourceChunk.text.strip()

            textChunk=review.find('div',{'class':'the_review'})
            if textChunk: text=textChunk.text.strip()

            dateChunk=review.find('div',{'class':'review-date subtle small'})
            if dateChunk: date=dateChunk.text.strip()

            csv_review.writerow([critic,rating,source,text,date]) # write to file 

    file_1.close()


url= 'https://www.rottentomatoes.com/m/enola_holmes/reviews'
Scrapper(url)



