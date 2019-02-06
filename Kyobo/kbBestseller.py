import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver # selenium은 webdriver api를 통해 브라우저를 제어함
from selenium.webdriver.common.by import By #https://www.seleniumhq.org/docs/03_webdriver.jsp#locating-ui-elements-webelements
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
# 교보문고 베스트셀러 페이지로 가기
main_url ='http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=d79'

driver=webdriver.Chrome("C:/driver/chromedriver.exe")
driver.get(main_url)
driver.implicitly_wait(3)

try:
    for page in range(1, 10):
        driver.execute_script("javascript:_go_targetPage('%s')" % page)
        time.sleep(2)
        print("%s 페이지 이동" % page)
        
        bestseller = []
        for i in range(0,19):
                findurl = (driver.find_elements_by_xpath('//*[@id="main_contents"]/ul/li[*]/div[2]/div[2]/a'))[i].get_attribute('href')
                driver.get(findurl)
                isbnInfo = (driver.find_element_by_xpath('//*[@id="container"]/div[5]/div[1]/div[3]/table/tbody/tr[1]/td/span[1]')).text
                bookdic = {
                    'isbn': str(isbnInfo)
                }
                bestseller.append(bookdic)
                driver.back()

        for list in bestseller:
            for key, value in list.items():
                print(key, ':', value)
        


except Exception as e:
        print("페이지 파싱 에러", e)
finally:
    time.sleep(5)
    driver.close()
