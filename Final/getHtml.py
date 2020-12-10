import csv, requests, os, time
BASE_URL = 'https://www.indeed.com'

def loadCSV(filePath):
    urls = []
    with open(filePath, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader:
            urls.append(line[1])
    return urls

def downloadHTML(filepath, link):
    with open(filepath, 'w') as file:
        html  = requests.get(BASE_URL+link).text
        file.write(html)

def run(csvpath):
    urls = loadCSV(csvpath)
    position = csvPath.split('/')[-1].split('.')[0]
    savePath = 'data/HTML/{}'.format(position)

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    for i in range(len(urls)):
        filePath = '{}/{}.html'.format(savePath,i)
        downloadHTML(filePath, urls[i])
        print('Scraped file: {}, {}\n'.format(i, urls[i]))
        time.sleep(1)

csvPath = 'data/CSV/Software_Engineer.csv'
run(csvPath)


