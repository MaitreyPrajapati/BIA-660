#Input : filepath to lexicon
#Returns : set of lexicon words
def loadLexicon(filePath):
    s = set()
    with open('positive-words.txt', 'r') as file:
        for word in file:
            s.add(word.strip())
    return s

def addToDict(words_after_positive, next_word):
    if(next_word in words_after_positive):
        words_after_positive[next_word] += 1
    else:
        words_after_positive[next_word] = 1

#Input : filePath-positveWords, filePath-inputFile        
def findMostOccuringWord(positivePath, textFilePath):
    words_after_positive = {}
    pos = loadLexicon(positivePath)
    
    with open(textFilePath) as text_file:
        for line in text_file:
            words = line.lower().strip().split(' ')
            for i in range(len(words)-1):
                if(words[i] in pos):
                    addToDict(words_after_positive, words[i+1])

    return max(words_after_positive, key=words_after_positive.get)

if __name__ == '__main__':
    print(findMostOccuringWord('positive-words.txt', 'textfile'))

