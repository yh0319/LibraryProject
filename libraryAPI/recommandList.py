from bs4 import BeautifulSoup
import requests
import time
import json
import pymongo
import re

def main():
    session = requests.session()
    with open('isbn.txt', "r", encoding="utf-8") as f:
        isbnList = []
        for i in f.readlines():
            i = i.replace('\n', '')
            i = i.replace(' ', '')
            isbnList.append(i)

    mainURL = 'http://data4library.kr/api/recommandList?authKey='
    API_KEY = "f2b79adb5d197d49b9d90cb2a7863b70cb6fac6299e8b94ec804b8749e6e6991"

    urls = scrape_list_page(mainURL, API_KEY, isbnList)


    recommandList = []
    for url in urls:
        time.sleep(1)
        response = session.get(url)
        bookInfo = scrape_detail_page(response)
        recommandList.append(bookInfo)
    
    print(recommandList)

    with open("recommandList.json", "w", encoding="utf-8-sig") as f:
        json.dump(recommandList, fp=f, ensure_ascii=False, indent=3)


def scrape_list_page(mainURL, API_KEY, isbnList):
    for isbn in isbnList:
        url = "{}{}&isbn13={}".format(mainURL,API_KEY,isbn)
        print(url)
        yield url

def scrape_detail_page(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        bookInfo = []
        for i in range(5):
            keyword = soup.select("isbn13")[0].string
            bookname = soup.select("bookname")[i].string
            author =soup.select("authors")[i].string
            publisher = soup.select("publisher")[i].string
            publication_year = soup.select("publication_year")[i].string
            isbn = soup.select("isbn13")[i+1].string

            dict = {
                'keyword' : keyword,
                'isbn' : isbn,
                'bookname' : bookname,
                'author': author,
                'publisher': publisher,
                'publication_year' : publication_year
            }
            bookInfo.append(dict)
        return bookInfo
        
    except Exception as e:
        print("페이지 파싱 에러", e)

if __name__ == "__main__":
    main()


