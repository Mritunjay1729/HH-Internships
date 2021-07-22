# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 13:49:13 2021

@author: MRITYUNJAY
facebookscraper
"""

import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from datetime import datetime

#input your email
email = "mritunjayaman28@gmail.com"
#input your password
passwd = "golduloveslovely"
#Your Query
topic = "ISEL Global"

options = ChromeOptions()
options.use_chromium = True
driver = Chrome(options = options)
driver.get("https://www.facebook.com")
username = driver.find_element_by_xpath('//input[@name="email"]')
username.send_keys(email)
password = driver.find_element_by_xpath('//input[@name="pass"]')
password.send_keys(passwd)
password.send_keys(Keys.RETURN)

search = driver.find_element_by_xpath('//input[@type="search"]')
search.send_keys(topic)
search.send_keys(Keys.RETURN)

cards = driver.find_elements_by_xpath('//div[@role="feed"]')
link = cards[0].find_element_by_xpath('.//a')
link.send_keys(Keys.RETURN)

driver.find_element_by_link_text('Reviews').click()

comment_list = []
names = []
dates = []

tokens = driver.find_elements_by_xpath('//div[@aria-posinset]')
tokens[0]
len(tokens)


for i in [23, 24, 48, 49]:
    all_comments = tokens[23].find_elements_by_xpath('.//div[@style="text-align: start;"]')
    comments = ""
    for j in all_comments:
        comments += " " + j.text
    comment_list.append(comments)
    name = tokens[23].find_element_by_xpath('.//h2[@id]').text
    names.append(name)
    date = tokens[23].find_element_by_xpath('.//span[@id]').text
    date = date.replace("\n", "")
    date = date.split(" ")
    month=""
    day=""
    year=""
    try:
        for i in date[1]:
            if(i.isdigit()):
                day += i
    except IndexError:
        day = ""
    try:
        for i in date[2]:
            if(i.isdigit()):
                year+=i
    except IndexError:
        year=""
    for i in range(len(date[0])):
        if(date[0][i].isupper()):
            month = date[0][i::]
            break
    new_date = month + " " + day + ", "+year
    dates.append(new_date)
    
print(len(comment_list), len(names), len(dates))
    
len(comment_list)

import pandas as pd
data = pd.DataFrame(dict(Name = names, Comment_date=dates, Comments = comment_list))
data.to_csv('fbISELGlobal.csv')
data['Name'].drop_duplicates(inplace = False)
#5 out of 5 based on ratings of 65 people
data.drop_duplicates(subset ="Name", keep = False, inplace = True)
data
