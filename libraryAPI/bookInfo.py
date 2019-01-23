from bs4 import BeautifulSoup
import requests
import timefrom bs4 import BeautifulSoup
import requests
import time
import json
import pymongo
import re

def main():
    session = requests.session()
    with open('isbn\isbn5.txt', "r", encoding="utf-8") as f:
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

    

    
    print(newBookInfo)

    # 크롤링 할 때마다 명칭 변경 필수
    with open("bookInfo4.json", "w", encoding="utf-8-sig") as f:
        json.dump(newBookInfo, fp=f, ensure_ascii=False, indent=3)


def scrape_list_page(mainURL, API_KEY, isbnList):
    for isbn in isbnList:
        url = "{}{}&isbn13={}&loaninfoYN=Y".format(mainURL,API_KEY,isbn)
        print(url)
        yield url

def scrape_detail_page(response):
    try:
        soup = BeautifulSoup(response.content, features='xml')
        bookInfo = []

        # for 0 in range(len(soup.select("bookname"))):
        isbn = soup.find("isbn13").text
        bookname = soup.find("bookname").text
        classno = soup.find("class_no").text
        author = soup.find("authors").text
        publisher = soup.find("publisher").text
        publication_year = soup.find("publication_year").text
        bookImage = (soup.find("bookImageURL")).text
        description = soup.find("description").text
        if soup.find("loanCnt") is None:
            LoanCnt = '' 
        else: 
            LoanCnt = soup.find("loanCnt").text
       
       
        dict = {
            'isbn' : isbn,
            'classno' : classno,
            'bookname' : bookname,
            'author': author,
            'publisher': publisher,
            'publication_year' : publication_year,
            'bookImage': bookImage,
            'description' : description,
            'loanCnt' : LoanCnt
        }
        bookInfo.append(dict)
        return bookInfo
        
    except Exception as e:
        print("페이지 파싱 에러", e)

if __name__ == "__main__":
    main()
