"""
Reads a list of reviews and decide if each review is positive or negative,
based on the occurences of positive and negative words.
"""

#function that loads a lexicon of positive words to a set and returns the set
def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())# remember to strip to remove the lin-change character
    lex_conn.close()

    return newLex

#function that reads in a file with reviews and decides if each review is positive or negative
#The function returns a list of the input reviews, a list of the respective decisions, and the positive & negative words found in each review
def run(path):
    decisions=[] 
    reviews=[]
    sentiwords=[]
    
    #load the positive and negative lexicons
    posLex=loadLexicon('positive-words.txt')
    negLex=loadLexicon('negative-words.txt')
    
    fin=open(path)
    for line in fin: # for every line in the file (1 review per line)
        posListInLine=[] #list of positive words in the review
        negListInLine=[] #list of negative words in the review
        
        reviews.append(line.strip())
        
        line=line.lower().strip()   
        
        words=line.split(' ') # slit on the space to get list of words
   
        for word in words: #for every word in the review
            if word in posLex: # if the word is in the positive lexicon
                posListInLine.append(word) #update the positive list for this review
            elif word in negLex: # if the word is in the negative lexicon
                negListInLine.append(word) #update the negative list for this review

        sentiwords.append([posListInLine,negListInLine])
    
        decision=0  # 0 for neutral    
        if len(posListInLine)>len(negListInLine): # more pos words than neg
            decision=1 # 1 for positiv
        elif len(negListInLine)>len(posListInLine):  # more neg than pos
            decision=-1 # -1 for negative
        decisions.append(decision)
            
        
    fin.close()
    return reviews, decisions,sentiwords


if __name__ == "__main__": 
    reviews,decisions,sentiwords=run('textfile')
    for i in range(len(reviews)):
        print(reviews[i], decisions[i],sentiwords[i])
       





