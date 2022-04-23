# exchenge https://coinmarketcap.com/rankings/exchanges/
# coindar https://coindar.org/ru/search?type=1&text=&start=2022-03-28&end=2022-03-28&tags=9&hot=0&rp=0&fav=0&coins=&cap_from=0&cap_to=600000000000&vol_from=0&vol_to=300000000000&ex=&sort=2&order=1

import requests
from bs4 import BeautifulSoup
import datetime
import base
import time

db = base.Base("localhost")


# print(requests.get("").text)

def CoinMarcetCapAnalitic(fullCoinName):
    url = "https://www.google.com/search?q=" + fullCoinName + "coinmarketcap"

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
    google = requests.get(url, headers=headers)
    soup = BeautifulSoup(google.text, 'lxml')
    linkToCoin = soup.find('div', class_="yuRUbf").find("a").get("href")
    print(linkToCoin + "markets/")

    cmc = requests.get(linkToCoin + "markets/", headers=headers)
    soup2 = BeautifulSoup(cmc.text, 'lxml')
    price = soup2.find('div', class_="priceValue").find("span").text
    market1 = soup2.find_all('div', class_="sc-16r8icm-0 jKrmxw container")

    print(market1)

    return price


def getListFromDate(date):
    lists = []

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
    url = f'https://coindar.org/ru/search?type=1&text=&start={date}&end={date}&tags=9&hot=0&rp=0&fav=0&coins=&cap_from=0&cap_to=600000000000&vol_from=0&vol_to=300000000000&ex=&sort=2&order=1'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_="event")

    for q in quotes:
        ball = 0
        tweet = 0
        source = 0
        today = False
        title = q.find('h3').find("a").text.split()

        if title[0] == "Листинг":
            coinName = q.find('h2').text.split()
            link = "https://coindar.org" + q.find('h3').find("a").get("href")
            like = int(q.find('span', class_="fav").text)
            response1 = requests.get(link)
            soup1 = BeautifulSoup(response1.text, 'lxml')
            quotes1 = soup1.find_all('div', class_="block-event")
            exProc = getEx(" ".join(title).replace("Листинг на бирже ", ""))

            for q1 in quotes1:
                addNewsDate = q1.find_all("div", class_="tool-rel")[1].text.split()
                source = "https://coindar.org" + q1.find("div", class_="date").find("a").get("href")

                try:
                    img = "https://coindar.org" + q1.find("div", class_='gallery_').find("a").get("href")
                except:
                    img = 0

                try:
                    tweet = q1.find("div", class_="tweet").find("div", class_="text").text
                except:
                    pass

                try:
                    reliability = int(q1.find("div", class_="ts_container").text.split()[0])
                except:
                    reliability = 0

            # addNewsDate[1].split(".").reverse()

            if tweet != 0:
                ball += 1

            if img != 0:
                ball += 1

            if exProc >= 0.75:
                ball += 1

            if reliability == 10:
                ball += 1


            addData = addNewsDate[1].split(".")

            addData.reverse()
            addData = "-".join(addData)

            if date == addData:
                ball += 1
                today = True

            lists.append({"title": " ".join(title),
                          "coinName": {"full": " ".join(coinName),
                                       "tiker": coinName[len(coinName) - 1]},
                          "exchenge": " ".join(title).replace("Листинг на бирже ", ""),
                          "date": date,
                          "like": like,
                          "balls": ball,
                          "exProc": exProc,
                          "today": today,
                          "addNewsDate": addNewsDate,
                          "reliability": reliability,
                          "source": source,
                          "img": img,
                          "link": link,
                          "tweet": tweet
                          })

    return lists


def getEx(exchenge):
    exlist = []
    url = "https://coinmarketcap.com/rankings/exchanges/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.find('tbody')
    i = 0
    fin = 0

    for t in tbody:
        i += 1
        tstmass = t.find_all("span", text=True)
        ex = str(tstmass).replace("[<span>", "").replace("</span>]", "")

        exlist.append({"ex": ex, "num": i})
        # print(f"{t} {i}")

    for e in exlist:
        if e["ex"] == exchenge:
            fin = 1 - (int(e["num"]) / len(exlist))
            # print(f"{e['ex']} {exchenge} {fin}")

    if fin == 0:
        return 1
    else:
        return fin


def cikle():
    today = datetime.datetime.today().date()
    listings = getListFromDate(str(today))
    for l in listings:
        if l["today"] == True and l["balls"] >= 4:
            db.postListing(l, 1)
        elif l["today"] == True and l["balls"] <= 3 and l["like"] < 50:
            db.postListing(l, 3)
        elif l["today"] == True and l["balls"] <= 3 and l["like"] >= 50:
            db.postListing(l, 2)
    time.sleep(15)


# getEx()

def errorsreturner():
    print("start")
    iteration = 1
    while True:
        print(f"Iteration number {iteration}....\n")
        iteration += 1
        cikle()


if __name__ == "__main__":
    while True:
        try:
            errorsreturner()
        except:
            print("errrors wtf mzfck")
            time.sleep(3)
            pass
