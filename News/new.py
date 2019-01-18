import time
import requests
import lxml.html
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By #https://www.seleniumhq.org/docs/03_webdriver.jsp#locating-ui-elements-webelements

#검색 page가 로딩 되는 시간을 대기하기 위한 모듈
from selenium.webdriver.support.ui import WebDriverWait

# 예외 처리를 위한 모듈
from selenium.webdriver.support import expected_conditions as EC

main_url = "https://news.naver.com/main/ranking/popularDay.nhn"

driver = webdriver.Chrome("C:/driver/chromedriver.exe")
driver.get(main_url)
time.sleep(3)
driver.implicitly_wait(10) # seconds

# 1. crawling 하는 시점의 날짜 headlines
article1_list = driver.find_elements_by_css_selector(".ranking_category_item a")
article1_urls = [item.get_attribute('href') for item in article1_list]
i = 1
for article in article1_urls:
    try:
        driver.get(article)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print(article)
        headlines = soup.select('.ranking_headline a')
        for headline in headlines:
            print('===== ', i, ' =====')
            print(headline.text)
            i += 1
    except:
        pass

# 2. crawling 하는 시점의 하루 전 날짜 headlines
print('=======================')
driver.get(main_url)
date_list = driver.find_elements_by_css_selector('.pagenavi_day a')
date_urls = [item.get_attribute('href') for item in date_list]

article_list = driver.find_elements_by_css_selector(".ranking_category_item a")
article_urls = [item.get_attribute('href') for item in article_list]

# i = 1
for date in date_urls:
    driver.get(date)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(date)
    for article in article_urls:
        try:
            driver.get(article)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # print('===== 2. category 별 URL 주소 =====')
            # print(article)
            headlines = soup.select('.ranking_headline a')
            for headline in headlines:
                print('======', '3 - ', i, '', '=====')
                print(headline.text)
                i += 1
        except:
            pass

time.sleep(3)
driver.close()