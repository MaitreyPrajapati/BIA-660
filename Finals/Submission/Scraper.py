from urllib.parse import urlparse

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions, expected_conditions
from selenium.webdriver.common.by import By  
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException,ElementNotInteractableException
from bs4 import BeautifulSoup
import time
import requests
import re


import csv
file_1 = open('Indeed.csv','w',encoding='utf8')
csv_review = csv.writer(file_1,lineterminator='\n')
csv_review.writerow(['Name','Text'])
file_link = open('links.txt','a',encoding='utf8')

# specifies the path to the chromedriver.exe
num_of_jobs = 0
page_num = 0  
driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://www.indeed.com/?from=gnav-homepage'
driver.get(url)
cities = ['Santa Clara,CA','Santa Clara,CA','Sunnyvale, CA','Cupertino, CA' ,'Queens,NY', 'Salem, MA', 'King of Prussia, PA',' Yardley,PA','Oakland, CA']
text = []
title= [] 
for i in cities:
    driver.find_element_by_id("text-input-where").click()
    driver.find_element_by_id("text-input-where").send_keys(Keys.CONTROL + "a")
    driver.find_element_by_id("text-input-where").send_keys(Keys.DELETE)
    time.sleep(3)
    driver.find_element_by_xpath( "//*//*[@id='text-input-where']").send_keys(i)

    job_fill = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='text-input-what']"))).send_keys('Data Engineers')
    
    driver.find_element_by_xpath("//*[@id='text-input-what']").send_keys(Keys.RETURN)
    
    driver.find_element_by_xpath("//*[@id='filter-distance']/button").click()

    driver.find_element_by_xpath("//*[@id='filter-distance-menu']/li[7]/a").click()
   

    try:
            while True:
                #
                try:
                    #time.sleep(5)
                    t='NA'
                    t=driver.find_element_by_xpath("/html/body/div[4]/div[1]/button")
                    if t!='NA':
                        time.sleep(1)
                        t.click(2)   
                        
                except NoSuchElementException:
                    pass
                responses = driver.page_source
                soup_people = BeautifulSoup(responses,'lxml')
                print(driver.find_element_by_xpath("//*[@id='searchCountPages']").text)
                with open('Indeed.csv','a',encoding='utf8',newline='') as file_2:

                    time.sleep(2)
                    home = driver.current_url
                    for j in soup_people.findAll('a',{'data-tn-element':'jobTitle'}):
                            # driver.switch_to.window(driver.window_handles[1])
                            link = "https://www.indeed.com" + j.get('href')
                            #print(link)
                            file_link.write(link + "\n")                        
                            driver.get(link) 
                            responses1 = driver.page_source
                            soup_desc = BeautifulSoup(responses1,'lxml')
                            num_of_jobs = num_of_jobs + 1
                            if num_of_jobs % 10 ==0:
                                time.sleep(1)
                            time.sleep(3)
                            position = soup_desc.find('div',{'class':'jobsearch-JobInfoHeader-title-container'}).text
                            try:
                                company = soup_desc.find('div',{'class':'jobsearch-CompanyReview--heading'}).text
                            except AttributeError :
                                company = soup_desc.find('div',{'class':'icl-u-lg-mr--sm icl-u-xs-mr--xs'}).text
                            desc = soup_desc.find('div',{'class' : 'jobsearch-jobDescriptionText'}).text
                            file_html = open(f'File_{str(num_of_jobs)}D.html','w',encoding='utf8')
                            file_html.write(responses1)
                            
                            csv_review.writerow([position,company,desc])
                            print(num_of_jobs)
                            time.sleep(1)
                    
                    driver.get(home)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    try:
                        next_page = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[aria-label=Next]"))).click()
                        continue
                    except (NoSuchElementException,TimeoutException):
                            break
    except NoSuchElementException:
        print("Website is waiting for captcha")
        time.sleep(50)
