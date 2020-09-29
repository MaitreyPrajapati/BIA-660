"""
A scriptthat reads a file from the web and returns the K most frequent words in the file
"""

import re
from nltk.corpus import stopwords
import requests
from operator import itemgetter

def run(url,K): 

    freq={} # keep the freq of each word in the file 

    stopLex=set(stopwords.words('english')) # build a set of english stopwrods 

    for i in range(5): # try 5 times
        
        #send a request to access the url
        response=requests.get(url,headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })    
        if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
            break # we got the file, break the loop
        else: print ('failed attempt',i)
     
    # all five attempts failed, return  None
    if not response: return None
    
    text=response.text# read in the text from the file
 
    text=re.sub('[^a-z]',' ',text.lower()) # replace all non-letter characters  with a space
    words=text.split(' ') # split to get the words in the text 

    for word in words: # for each word in the sentence 
        if word=='' or word in stopLex:continue # ignore empty words and stopwords 
        else: freq[word]=freq.get(word,0)+1 # update the frequency of the word 
            
    # sort the dictionary by value, in descending order 
    sortedByValue=sorted(freq.items(),key=itemgetter(1),reverse=True)
    
    return sortedByValue[0:K] # return the top K terms and their frequencies 

        
print(run('https://gist.githubusercontent.com/corydolphin/d2d76dae81df22a18d036244979c3c7b/raw/f3237ee708b4f685a5e5ded3514afcf0863768aa/Speech.txt',3))


"""
Use this to install stopwords:
import nltk
nltk.download()
"""