# coding: utf-8

import urllib.request, time
from bs4 import BeautifulSoup
import pandas as pd

my_header = {
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Language': 'zh-TW,zh;q=0.9,zh-CN;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

def getUrls():
    urls = []
    for i in range(1,21):
        url = 'https://www.itjuzi.com/investevents?page=%d' % i
        urls.append(url)
    return urls

def getInfo():
    company = []; label = []; location = []; rounds = []; money = []
    contents = {}
    for url in getUrls():
        time.sleep(2)
        print(url)
        req = urllib.request.Request(url, headers = my_header)
        res = urllib.request.urlopen(req)
        html = (res.read()).decode()
        soup = BeautifulSoup(html, 'html.parser')
        for company_s in soup.select('.title a span'):
            company.append(company_s.text)
            print(company_s.text)
        for label_s in soup.select('.tags a'):
            label.append(label_s.text)
            print(label_s.text)
        for location_s in soup.select('.loca a'):
            location.append(location_s.text)
            print(location_s.text)
        for rounds_s in soup.select('.gray'):
            rounds.append(rounds_s.text)
            print(rounds_s.text)
        for money_s in soup.select('.money')[1:]:
            money.append(money_s.text)
            print(money_s.text)
    contents['company'] = company; contents['label'] = label;
    contents['location'] = location; contents['rounds'] = rounds; contents['money'] = money
    return contents

def getIndex():
    date = []
    for url in getUrls():
        req = urllib.request.Request(url, headers = my_header)
        res = urllib.request.urlopen(req)
        html = (res.read()).decode()
        soup = BeautifulSoup(html, 'html.parser')
        for date_s in soup.select('.date span'):
            date.append(date_s.text)
    return date
    
df = pd.DataFrame(getInfo(), index = getIndex(), columns = ['location', 'label', 'company', 'money', 'rounds'])
df.to_excel('data-1.xlsx')