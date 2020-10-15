from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import csv
import re

BASE_URL = 'https://www.amazon.com/product-reviews/'
REGEX_PATTERN = 'a\-star\-[1-5]'

def loadLink(p_code):
    driver = webdriver.Chrome('chromeDriver/chromedriver')
    review_set = set()
    review_list = []
    link = BASE_URL + p_code

    while(link):
        driver.get(link)
        reviews = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-hook="review"]')))
        for review in reviews:
            ratings = re.search(REGEX_PATTERN, review.find_element_by_css_selector('i[data-hook$="review-star-rating"]').get_attribute('class')).group(0)[-1]
            text = review.find_element_by_css_selector('span[data-hook="review-body"]').text
            if((ratings, text) not in review_set):
                review_set.add((ratings, text))
                review_list.append((ratings, text))

        next_page_link = driver.find_element_by_css_selector('div[data-hook="pagination-bar"]').find_element_by_class_name('a-last')

        if('a-disabled' in next_page_link.get_attribute('class')):
            break
        else:
            link = next_page_link.find_element_by_css_selector('*').get_attribute('href')

    return review_list

def scrape(link):
    p_code = link.strip().split('/')[-1]
    review_list = loadLink(p_code)

    with open('reviews.csv', 'w') as file:
        csv_writer = csv.writer(file, delimiter=',')

        for (ratings, text) in review_list:
            csv_writer.writerow([ratings, text])



link = 'https://www.amazon.com/Sennheiser-Momentum-Cancelling-Headphones-Functionality/dp/B07VW98ZKG'
scrape(link)
