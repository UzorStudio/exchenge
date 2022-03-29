# exchenge https://coinmarketcap.com/rankings/exchanges/
# coindar https://coindar.org/ru/search?type=1&text=&start=2022-03-28&end=2022-03-28&tags=9&hot=0&rp=0&fav=0&coins=&cap_from=0&cap_to=600000000000&vol_from=0&vol_to=300000000000&ex=&sort=2&order=1

import requests
from bs4 import BeautifulSoup
import datetime


# print(requests.get("").text)

def CoinMarcetCapAnalitic(fullCoinName):
    url = "https://www.google.com/search?q="+fullCoinName+"coinmarketcap"

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
    google = requests.get(url, headers=headers)
    soup = BeautifulSoup(google.text, 'lxml')
    linkToCoin = soup.find('div', class_="yuRUbf").find("a").get("href")
    print(linkToCoin+"markets/")

    cmc = requests.get(linkToCoin+"markets/", headers=headers)
    soup2 = BeautifulSoup(cmc.text, 'lxml')
    price = soup2.find('div',class_="priceValue").find("span").text
    market1 = soup2.find_all('div',class_="sc-16r8icm-0 jKrmxw container")

    print(market1)


    return price

def getListFromDate(day, month, year):
    lists = []
    date = f"{year}-{month}-{day}"

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
    url = f'https://coindar.org/ru/search?type=1&text=&start={date}&end={date}&tags=9&hot=0&rp=0&fav=0&coins=&cap_from=0&cap_to=600000000000&vol_from=0&vol_to=300000000000&ex=&sort=2&order=1'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_="event")

    for q in quotes:
        title = q.find('h3').find("a").text.split()
        coinName = q.find('h2').text.split()
        link = "https://coindar.org" + q.find('h3').find("a").get("href")
        like = q.find('span', class_="fav").text
        if title[0] == "Листинг":

            response1 = requests.get(link)
            soup1 = BeautifulSoup(response1.text, 'lxml')
            quotes1 = soup1.find_all('div', class_="block-event")

            for q1 in quotes1:
                addNewsDate = q1.find_all("div", class_="tool-rel")[1].text.split()
                try:
                    img = "https://coindar.org" + q1.find("div",class_='gallery_').find("a").get("href")
                    reliability = int(q1.find("div", class_="ts_container").text.split()[0])
                except:
                    reliability = "in link"

            lists.append({"title": " ".join(title),
                          "coinName": {"full": " ".join(coinName),
                                       "tiker": coinName[len(coinName) - 1]},
                          "exchenge": " ".join(title).replace("Листинг на бирже ", ""),
                          "date": date,
                          "like": like,
                          "addNewsDate": addNewsDate,
                          "reliability": reliability,
                          "img":img,
                          "link": link
                          })

    return lists


def getEx():
    url = "https://coinmarketcap.com/rankings/exchanges/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_="block-event")


listings = getListFromDate(day=29, month="03", year=2022)

for l in listings:
    coinname = l["coinName"]["full"]
    print(CoinMarcetCapAnalitic(coinname))
    break
