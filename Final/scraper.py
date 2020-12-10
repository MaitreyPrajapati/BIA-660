from bs4 import BeautifulSoup
import requests, csv, os, sys

BASELINK = 'https://www.indeed.com/jobs?q='
INDEED_HOME = 'https://www.indeed.com/'
CITY_SPLITTER = '%2C+'

HEADERS =  {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}

visited = set()
counter = 0

## CSV Format - post, location, url
def loadVisted(path):
    if(os.path.exists(path)):
        with open(path) as file:
            reader = csv.reader(file, delimiter=',')
            for (_, __, url) in reader:
                visited.add(url)
        return
    print("CSV doesn't exist - {}\n\n".format(path))


def loadCSV(path, location, urlArr):
    if not os.path.exists('data/CSV'):
        os.makedirs('data/CSV')

    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=',')
        for i in urlArr:
            writer.writerow([location, i])

def getBS(link):
    for i in range(5):
        try:
            res = requests.get(link, HEADERS)
            if not res:
                print('Proxy worked but couln not find link : {}'.format(link))
                continue
            return BeautifulSoup(res.text, 'lxml')
        except:
            continue

def getJobs(link, jobs):
    curr_pass = []
    for i in range(0, min(1000, jobs), 10):
        try:
            curr = getBS(link + '&start=' + str(i))
            if not curr:
                print('Can not find link {} at start{}'.format(link, i))
                return
            jobs = curr.select('a[class="jobtitle turnstileLink"]')
            for j in jobs:
                job_link = j['href']
                if job_link not in visited:
                    visited.add(job_link)
                    curr_pass.append(job_link)
                    if counter == 5000:
                        break
            return curr_pass
        except:
            print('could not get the url : {}'.format(link))
            return

def run(locations, position):
    filePath = 'data/CSV/{}.csv'.format(position.replace(' ', '_'))
    loadVisted(filePath)
    counter = len(visited)
    for (city, state) in locations:
        if counter < 5000:
            link = BASELINK + position.replace(' ', '+')+'&l=' + city.replace(' ', '+') + CITY_SPLITTER + state
            preetydata = getBS(link)
            if preetydata:
                try:
                    print(link)
                    jobs = int(preetydata.find('div', {'id': 'searchCountPages'}).text.strip().split(' ')[-2].replace(',',''))
                    curr_pass = getJobs(link, jobs)
                    loadCSV(filePath, '{}, {}'.format(city, state), curr_pass)
                except:
                    print(sys.exc_info())

locations = [['Santa Clara', 'CA'],['Sunnyvale', 'CA'],['Cupertino', 'CA'], ['Queens', 'NY'], ['Salem', 'MA'], ['King of prussia', 'PA'], ['Yardley', 'PA'], ['Oakland', 'CA']]
position = 'Software Engineer'

run(locations, position)

