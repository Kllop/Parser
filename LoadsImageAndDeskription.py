from splinter import browser
from bs4 import BeautifulSoup

import time
import os
import json


nameData = 'Description.json'


def CheckDataItems():
    folderNames = os.listdir()
    for name in folderNames:
        if name == nameData:
            break
    else: 
        return False
    return True

data = []
VerifiedData = []
items = []

temp = open('data.json', 'r')
data = json.loads(temp.read())['result']
temp.close()

if CheckDataItems():
    temp = open(nameData, 'r')
    loadsData = json.loads(temp.read())

    if len(loadsData):
        fdata = data.copy()
        temp  = open('Verified.json', 'r')
        VerifiedData = json.loads(temp.read())
        temp.close()
        temp = open(nameData, 'r')
        items = json.loads(temp.read())
        for item in fdata:
            index = VerifiedData.index(item['pricepos_code'])
            print(index)
            if index != -1:
                data.remove(item['pricepos_code'])


browser = browser.Browser('chrome', incognito=True)
 

for item in data:
    browser.visit('https://apteka-ot-sklada.ru/catalog?q='+item['pricepos_code'])

    soup = BeautifulSoup(browser.html, 'html.parser')

    data = soup.find_all("div", class_="ui-card goods-card goods-grid__cell goods-grid__cell_size_3")
    if len(data) == 0:
        VerifiedData.append(item['pricepos_code'])
        jsdata = json.dumps(VerifiedData)
        temp = open('Verified.json', 'w')
        temp.write(jsdata)
        temp.close()
        continue
    
    soup = BeautifulSoup(str(data), 'html.parser')
    html = soup.find_all("a", href=True)
    browser.visit('https://apteka-ot-sklada.ru'+str(html[0]['href']))
    soup = BeautifulSoup(browser.html, 'html.parser')
    image = soup.find_all('img', class_ = 'goods-photo goods-gallery__picture')[0]['src']
    image = 'https://apteka-ot-sklada.ru' + image
    html = soup.find_all('div', class_ = 'custom-html content-html')[0]
    Description = html.get_text()
    writedata = dict(pricepos_name = item['pricepos_name'],
                     pricepos_count = item['pricepos_count'],
                     pricepos_value = item['pricepos_value'],
                     pricepos_country = item['pricepos_country'],
                     pricepos_code = item['pricepos_code'],
                     description = Description, 
                     image = image
                     )
    items.append(writedata)
    temp = open(nameData, 'w')
    jsdata = json.dumps(items)
    temp.write(jsdata)
    VerifiedData.append(item['pricepos_code'])
    jsdata = json.dumps(VerifiedData)
    temp = open('Verified.json', 'w')
    temp.write(jsdata)
    temp.close()
    time.sleep(2)


