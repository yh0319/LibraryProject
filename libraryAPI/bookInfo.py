from bs4 import BeautifulSoup
import requests
import time
import json
import pymongo
import re

def main():
    session = requests.session()
    with open('isbn1.txt', "r", encoding="utf-8") as f:
        isbnList = []
        for i in f.readlines():
            i = i.replace('\n', '')
            i = i.replace(' ', '')
            isbnList.append(i)

    mainURL = 'http://data4library.kr/api/srchDtlList?authKey='


    API_KEY = "[APIKEY]"

    urls = scrape_list_page(mainURL, API_KEY, isbnList)

    # headers = {'User-Agent':'' }
    newBookInfo = []
    for url in urls:
        time.sleep(1)
        response = session.get(url)
        bookInfo = scrape_detail_page(response)
        newBookInfo.append(bookInfo)
        break

    
    print(newBookInfo)

    # 크롤링 할 때마다 명칭 변경 필수
    with open("bookInfo.json", "w", encoding="utf-8-sig") as f:
        json.dump(newBookInfo, fp=f, ensure_ascii=False, indent=3)


def scrape_list_page(mainURL, API_KEY, isbnList):
    for isbn in isbnList:
        url = "{}{}&isbn13={}&loaninfoYN=Y".format(mainURL,API_KEY,isbn)
        print(url)
        yield url

def scrape_detail_page(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        bookInfo = []

        isbn = soup.select("isbn13").string
        bookname = soup.select("bookname").string
        classno = soup.select("class_no").string
        author =soup.select("authors").string
        publisher = soup.select("publisher").string
        publication_year = soup.select("publication_year").string
        bookImage = soup.select("bookImageURL").string
        description = soup.select("description").string
        totalLoanCnt = soup.select("loanCnt")[0].string

        dict = {
            'isbn' : isbn,
            'classno' : classno,
            'bookname' : bookname,
            'author': author,
            'publisher': publisher,
            'publication_year' : publication_year,
            'bookImage': bookImage,
            'description' : description,
            'loanCnt' : totalLoanCnt
        }
        bookInfo.append(dict)
        return bookInfo
        
    except Exception as e:
        print("페이지 파싱 에러", e)

if __name__ == "__main__":
    main()


