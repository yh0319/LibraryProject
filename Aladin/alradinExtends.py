import time
import re
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By 

# 예외 처리를 위한 모듈
from selenium.webdriver.support import expected_conditions as EC




# 드라이버 오픈
driver = webdriver.Chrome("C:/driver/chromedriver.exe")
url='https://www.aladin.co.kr/home/welcome.aspx#'
driver.get(url)


#아뒤와 비번을 변수로 지정
id = '아뒤'
pw = '비번'



login = driver.find_element_by_xpath('//*[@id="#head_myaccount_layer"]/div[1]/a/img')
# 로그인 로직

login.click()
time.sleep(5)
driver.find_element_by_name('Email').send_keys(id) # 값 입력
driver.find_element_by_name('Password').send_keys(pw)
time.sleep(5)
driver.find_element_by_class_name('button_login1_2016').click() #로그인 버튼 클릭
time.sleep(1)
driver.get(url) #홈페이지를 다시 가져온다. 


# 검색 로직
driver.find_element_by_id('SearchWord').send_keys("빅데이터")
time.sleep(4)
driver.execute_script("javascript:searchTargetChange('EBook','eBook',0)") #검색 시 리스트에 있던 통합검색을 ebook으로 변환
time.sleep(4)
driver.find_element_by_class_name('searchBtn').click() #검색 버튼 클릭
time.sleep(4)
driver.execute_script("javascript:ViewRowCount_Set('50')") #클릭 후 들어온 곳에 데이터 표시를 25개에서 50개로 바꿔줌
time.sleep(4)
#데이터베이스 연동에 활용할 리스트 생성
bookdata = []

try:
    for page in range(1, 3):
        driver.execute_script("Javascript:Page_Set('{}')".format(page))
        driver.implicitly_wait(5)
        print("{} 페이지입니다..".format(page))

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        boxItems = soup.select("#Search3_Result .ss_book_box")
        
        
        for boxItem in boxItems:
            img_src = boxItem.find("img")['src']
            link = boxItem.find("a")['href']
            title = boxItem.select("b")[0].text
            price = boxItem.select("b")[1].text
            price = price.replace(',','')
            price = re.search(r"(\w+)(원)", price).group(1)
            publisher = boxItem.select("li")[1].text

            print("상품명 :", title)
            print("가격 :", price)
            print("썸네일 :", img_src)
            print("링크 :", link)
            print("출판정보 :", publisher)
            print("==============================================")
            #출판 정보에서 문제발생 : 정규표현식 사용으로 저자/출판사/출간일을 나누려 했으나 데이터값이 서로 상이한 관계로 그룹화 찾기에 실패함

            bookdata.append({'title':title, 'price':price, 'publisher':publisher, 'link':link})
except Exception as e:
    print("페이지 파싱 에러", e)
finally:
    time.sleep(4)


#연동할 데이터베이스 생성
def create_db(db_path, bookdata):
    conn = sqlite3.connect(db_path)
    # 커서를 추출합니다.
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS bookdata')
    cur.execute('''
        CREATE TABLE bookdata (
            link text,
            title text,
            publisher text,
            price integer
        )
    ''')
    cur.executemany('INSERT INTO bookdata VALUES(:title, :publisher, :price, :link)', bookdata)
    conn.commit()
    conn.close()


create_db('abooks.db', bookdata)
driver.find_element_by_xpath('//*[@id="global_set3_2"]/ul/li[1]/a/img').click()
time.sleep(3)
driver.close()
