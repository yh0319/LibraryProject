from bs4 import BeautifulSoup
import requests
import time
import json
import pymongo
import re

def main():
    session = requests.session()
   
    mainURL = 'http://data4library.kr/api/loanItemSrch?authKey='
    API_KEY = "[API KEY를 입력하세요]"
    ageGroup = ['10', '20', '30', '40', '50', '60', '70']
    genderGroup = ['0','1']
    urls = scrape_list_gender(mainURL, API_KEY, genderGroup, ageGroup)
    
    popular_books_list = []
    
    for url in urls:
        time.sleep(1)
        response = session.get(url)
        bookInfo = scrape_detail_gender(response)
        popular_books_list.append(bookInfo)
    
    print(popular_books_list)

    with open("PopularBookBygender.json", "w", encoding="utf-8-sig") as f:
        json.dump(popular_books_list, fp=f, ensure_ascii=False, indent=3)

# 성별로 인기대출도서 결과 가져오기 위한 url 조합 및 호출
def scrape_list_gender(mainURL, API_KEY, genderGroup, ageGroup):
    for age in ageGroup:
        for gender in genderGroup:
            url = "{}{}&startDt=2018-01-01&age={}&gender={}".format(mainURL,API_KEY, age, gender)
            print(url)
            yield url

# 도서 정보 스크레핑
def scrape_detail_gender(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        bookInfo = []
        for i in range(len(soup.select("bookname"))):
            age = soup.select("age")[0].string
            ranking = soup.select("ranking")[i].string
            gender = soup.select("gender")[0].string
            bookname = soup.select("bookname")[i].string
            author =soup.select("authors")[i].string
            publisher = soup.select("publisher")[i].string
            publication_year = soup.select("publication_year")[i].string
            isbn = soup.select("isbn13")[i].string

            dict = {
                'bookname' : bookname,
                'author': author,
                'publisher': publisher,
                'gender' : gender,
                'age' : age,
                'ranking' : ranking,
                'isbn' : isbn,
                'publication_year' : publication_year
            }
            bookInfo.append(dict)
        return bookInfo
    except Exception as e:
        print("페이지 파싱 에러", e)

if __name__ == "__main__":
    main()


