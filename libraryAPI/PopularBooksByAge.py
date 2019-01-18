from bs4 import BeautifulSoup
import requests
import time
import json
import pymongo
import re

def main():
    session = requests.session()
    
    mainURL = 'http://data4library.kr/api/loanItemSrch?authKey='
    API_KEY = "[API키를 입력하세요]"
    ageGroup = ['10', '20', '30', '40', '50', '60', '70']
    urls = scrape_list_page(mainURL, API_KEY, ageGroup)


    popular_books_list = []
    for url in urls:
        time.sleep(1)
        response = session.get(url)
        bookInfo = scrape_detail_page(response)
        popular_books_list.append(bookInfo)
    
    print(popular_books_list)

    with open("PopularBookByAge.json", "w", encoding="utf-8-sig") as f:
        json.dump(popular_books_list, fp=f, ensure_ascii=False, indent=3)


def scrape_list_page(mainURL, API_KEY, ageGroup):
    for age in ageGroup:
        url = "{}{}&startDt=2018-01-01&age={}".format(mainURL,API_KEY, age)
        print(url)
        yield url

def scrape_detail_page(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        bookInfo = []
        for i in range(len(soup.select("bookname"))):
            age = soup.select("age")[0].string
            ranking = soup.select("ranking")[i].string
            bookname = soup.select("bookname")[i].string
            author =soup.select("authors")[i].string
            publisher = soup.select("publisher")[i].string
            publication_year = soup.select("publication_year")[i].string
            isbn = soup.select("isbn13")[i].string

            dict = {
                'bookname' : bookname,
                'author': author,
                'publisher': publisher,
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


