import csv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

LOGIN_PAGE = 'https://www.linkedin.com/login'
NETFLIX_PEOPLE = 'https://www.linkedin.com/company/netflix/people/'

driver = webdriver.Chrome('chromeDriver/chromedriver')

user = 'mockddmock@gmail.com'
passw = 'Parseword@2112'


def getPage(link):
    return driver.get(link)

def login(username, password):
    driver.get(LOGIN_PAGE)
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_css_selector('button[data-litms-control-urn="login-submit"]').click()

def getProfiles(link, location):

def run():
    login(user, passw)

run()


