import csv, time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

LOGIN_PAGE = 'https://www.linkedin.com/login'
college_links = [
                 'https://www.linkedin.com/company/netflix/people/',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17971',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17950',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=18993',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17939',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17926',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17911',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17831',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17959',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17875',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17954',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=18475',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17812',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=18461',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=19518',
                 'https://www.linkedin.com/company/netflix/people/?facetSchool=17947']

driver = webdriver.Chrome('chromeDriver/chromedriver')

### Need to change profile before visiting
user = 'maitrey2112@gmail.com'
passw = 'Parseword@2112'

def getVisitedLinks(file):
    visited = set()
    with open(file) as file:
        csv_reader = csv.reader(file, delimiter=',')
        for l in csv_reader:
            visited.add(l[0])
    return visited

visited = getVisitedLinks('links_1.csv')
if not visited:
    visited = set()

def login(username, password):
    driver.get(LOGIN_PAGE)
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_css_selector('button[data-litms-control-urn="login-submit"]').click()


def getProfiles(link):
    print('-----------------------------------------------------------------------\n Trying out link : {}\n\n'.format(link))
    driver.get(link)
    last_height, curr_height = 0, 1
    counter = len(visited)

    with open('links_1.csv', 'a') as file:
        csv_writer = csv.writer(file, delimiter=',')
        while( last_height != curr_height and counter<2000):
            last_height = driver.execute_script("return document.body.scrollHeight")
            profiles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[class="org-people-profiles-module__profile-item"]')))
            if profiles:
                for p in profiles:
                    plink = p.find_element_by_css_selector('div[class="artdeco-entity-lockup__title ember-view"]')
                    plink = plink.find_elements_by_css_selector('a')

                    if plink:
                        plink = plink[0].get_attribute('href')
                        if plink not in visited:
                            visited.add(plink)
                            csv_writer.writerow([plink])
                            counter+=1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            curr_height = driver.execute_script("return document.body.scrollHeight")

    if counter >= 2000:
        return True
    return False


def run():
    login(user, passw)
    for l in college_links:
        if getProfiles(l):
            break

run()


