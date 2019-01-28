from bs4 import BeautifulSoup
import requests
import time
import json
import pymongo
import re
import pandas as pd
import bson
from bson.raw_bson import RawBSONDocument

def main():
    session = requests.session()


    with open(r'C:\0.ITstudy\0.libraryAPI\watchaYH\unknown11.txt', "r", encoding="utf-8") as f:
        list = []
        for i in f.readlines():
            i = i.replace('\n', '')
            i = i.replace(' ', '')
            list.append(i)


  

    
    API_KEY = 'CA4B20C10CE7B07B8A0376F898EA32F24C0B956EFB0E5E7422A6886902CD8A21'
    mainurl = 'http://book.interpark.com/api/search.api?key='



    urls = scrape_list_page(list, mainurl, API_KEY)
    interpark_book_list = []
    
    for url in urls:
        time.sleep(1)
        response = session.get(url)
        bookInfo = scrape_detail_page(response)
        print(bookInfo)
        interpark_book_list.append(bookInfo)


    with open("unknown11.json", "w", encoding="utf-8-sig") as f:
        json.dump(interpark_book_list, fp=f, ensure_ascii=False, indent=3)





def scrape_list_page(list, mainurl, API_KEY):
    for query in list:
        url = "{}{}&query={}&maxResults=100&searchTarget=book&soldOut=n&queryType=title".format(mainurl, API_KEY, query)
        print(url)
        yield url

def scrape_detail_page(response):
    try:
        soup = BeautifulSoup(response.text,'html.parser') 
        bookInfo = []
        for i in range(len(soup.select("item"))):
            title = soup.select("item title")[i].string #제목
            date = soup.select("item pubdate")[i].string #출간일
            # categoryname = soup.select("item categoryname")[i].string #주제분류
            author = soup.select("item author")[i].string #저자
            publisher = soup.select("item publisher")[i].string #출판사
            isbn = soup.select("item isbn")[i].string #isbn code
            # translator = soup.select("item translator")[i].string #역자
            # id = soup.select("item itemid")[i].string #인터파크 고유번호
            image = soup.select("item coverlargeurl")[i].string #이미지
            # rate = soup.select("item customerreviewrank")[i].string #평점
            # review = soup.select("item reviewcount")[i].string #리뷰

            dict = {
                # 'id' : id,
                'title' : title,
                'date' : date,
                # 'categoryname' : categoryname,
                'publisher' : publisher,
                'author' : author,
                # 'translator' : translator,
                # 'rate' : rate,
                # 'review' : review,
                'isbn' : isbn,
                'image' : image,
            }
            bookInfo.append(dict)
            break
        return bookInfo
    except Exception as e:
        print("페이지 파싱 에러", e)





if __name__ == "__main__":
    main()