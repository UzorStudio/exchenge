
lohi = [1]

while True:
    lohi.append()


#def getListToday():
#    lists=[]
#    now = datetime.datetime.now()
#    date = f"{now.year}-{now.month}-{now.day}"
#
#    headers = {
#        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
#    url = f'https://coindar.org/ru/search?type=1&text=&start={date}&end={date}&tags=9&hot=0&rp=0&fav=0&coins=&cap_from=0&cap_to=600000000000&vol_from=0&vol_to=300000000000&ex=&sort=2&order=1'
#    response = requests.get(url, headers=headers)
#    soup = BeautifulSoup(response.text, 'lxml')
#    quotes = soup.find_all('div', class_="event")
#
#    for q in quotes:
#        title = q.find('h3').find("a").text.split()
#        coinName = q.find('h2').text.split()
#        link = "https://coindar.org" + q.find('h3').find("a").get("href")
#        like = q.find('span', class_="fav").text
#        if title[0] == "Листинг":
#            lists.append({"title":" ".join(title),
#                          "coinName":{"full":" ".join(coinName),
#                                      "tiker":coinName[len(coinName)-1]},
#                          "link":link,
#                          "exchenge":" ".join(title).replace("Листинг на бирже ",""),
#                          "date":date,
#                          "like":like
#                          })
#
#    return lists