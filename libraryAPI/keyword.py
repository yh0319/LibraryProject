from bs4 import BeautifulSoup
import requests
import time
import json
import pymongo
import re

def main():
    session = requests.session()
    with open('isbn\isbn1.txt', "r", encoding="utf-8") as f:
        isbnList = []
        for i in f.readlines():
            i = i.replace('\n', '')
            i = i.replace(' ', '')
            isbnList.append(i)

    mainURL = 'http://data4library.kr/api/keywordList?authKey='


    # API_KEY = "f2b79adb5d197d49b9d90cb2a7863b70cb6fac6299e8b94ec804b8749e6e6991"
    # 수연 API KEY
    # API_KEY = "316e5012b66d2e3fe66a04d6d6ef5521ef7ae6ace9b51476a433981b6d5a2c14"
    # 민석
    # API_KEY = "e810b7a07d7efcc9b31e97b89f9fd39755c1fe2e94a1a264a6767511e3c749df"
    # 원정
    API_KEY = "88fc64146e42d714120b9b4ffa7c49f2d7108a89af53773103fbb51c67385cc2"

    urls = scrape_list_page(mainURL, API_KEY, isbnList)

    # headers = {'User-Agent':'' }
    newKeyword = []
    for url in urls:
        time.sleep(1)
        response = session.get(url)
        keyword = scrape_detail_page(response)
        newKeyword.append(keyword)

    

    
    print(newKeyword)

    # 크롤링 할 때마다 명칭 변경 필수
    with open("keyword1.json", "w", encoding="utf-8-sig") as f:
        json.dump(newKeyword, fp=f, ensure_ascii=False, indent=3)


def scrape_list_page(mainURL, API_KEY, isbnList):
    for isbn in isbnList:
        url = "{}{}&isbn13={}&additionalYN=Y".format(mainURL,API_KEY,isbn)
        print(url)
        yield url

def scrape_detail_page(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        keyword = []
        for i in range(len(soup.select("word"))):
            word = soup.select("word")[i].string
            weight = soup.select("weight")[i].string
            isbn = soup.select("isbn13")[0].string
       
            dict = {
                'isbn' : isbn,
                'word' : word,
                'weight' : weight
            }
            keyword.append(dict)
        return keyword
        
    except Exception as e:
        print("페이지 파싱 에러", e)

if __name__ == "__main__":
    main()


