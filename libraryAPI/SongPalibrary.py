from bs4 import BeautifulSoup
import requests
import time
import json
import pymongo
import re

def main():
    session = requests.session()
    
    mainURL = 'http://data4library.kr/api/loanItemSrch?authKey='
    API_KEY = "f2b79adb5d197d49b9d90cb2a7863b70cb6fac6299e8b94ec804b8749e6e6991"
    years = []
    for i in range(16):
        i = 2004 + i
        years.append(i)

    urls = scrape_list_page(mainURL, API_KEY, years)

    popular_books_list = []
    for url in urls:
        time.sleep(1)
        response = session.get(url)
        bookInfo = scrape_detail_page(response)
        popular_books_list.append(bookInfo)
    
    print(popular_books_list)

    with open("SongPalibrary.json", "w", encoding="utf-8-sig") as f:
        json.dump(popular_books_list, fp=f, ensure_ascii=False, indent=3)



def scrape_list_page(mainURL, API_KEY, years):
    for year in years:
        url = "{}{}&startDt={}-01-01&endDt={}-12-12".format(mainURL,API_KEY, year, year)
        print(url)
        yield url

def scrape_detail_page(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        bookInfo = []
        for i in range(len(soup.select("bookname"))):
            bookname = soup.select("bookname")[i].string
            author =soup.select("authors")[i].string
            publisher = soup.select("publisher")[i].string
            publication_year = soup.select("publication_year")[i].string
            isbn = soup.select("isbn13")[i].string

            dict = {
                'bookname' : bookname,
                'author': author,
                'publisher': publisher,
                'isbn' : isbn,
                'publication_year' : publication_year
            }
            bookInfo.append(dict)
        return bookInfo
    except Exception as e:
        print("페이지 파싱 에러", e)

if __name__ == "__main__":
    main()



