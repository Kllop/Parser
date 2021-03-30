from splinter import browser
from bs4 import BeautifulSoup

import time
import os
import json


#login: apteka25892
#password: 7oRCC

#pricepos_name: Наименование товара
#pricepos_count: Количество
#pricepos_value: Цена
#pricepos_country: Страна производитель
#pricepos_code: id товара 

def CheckDataAuthorization():
    FolderNames = os.listdir()
    for name in FolderNames:
        if name == "Authorization.json":
            break
    else:
        login = input("Ведите логин для авторизации: ")
        password = input("Ведите пороль для авторизации: ")
        data = {'login': login, 'password': password}
        jsdata = json.dumps(data)
        temp = open('Authorization.json', 'w')
        temp.write(jsdata)
        temp.close()



CheckDataAuthorization()
temp = open("Authorization.json", 'r')
data = json.loads(temp.read())

#executable_path = {'executable_path': os.getcwd()+"/chromedriver"}
login = data['login']
password = data['password']


browser = browser.Browser('chrome', incognito=True)

browser.visit('https://zakaz.godovalov.ru/')

browser.reload()

browser.fill('login', login)

browser.fill('password', password)

browser.click_link_by_id('ext-gen1022')

browser.visit('https://zakaz.godovalov.ru/ordersale')

time.sleep(20)

browser.visit('https://zakaz.godovalov.ru/priceposlist_json?ordersale_id')

page = browser.html

soup = BeautifulSoup(page, 'html.parser')
data = soup.get_text()

temp = open('data.json', 'w')
jsdata = json.loads(temp)
data = jsdata['result']
temp.write(data)
temp.close()

time.sleep(10)
