#!/usr/bin/env python
# coding: utf-8

#%pip install selenium
from selenium import webdriver
import time 
import random
from bs4 import BeautifulSoup
import requests
import pandas as pd 


url = 'https://www.flightaware.com/live/aircrafttype/A320'
#url = 'https://www.flightaware.com/live/cancelled/'

#Chose which browser to use: 
#cService = webdriver.ChromeService(executable_path='/snap/bin/firefox.geckodriver')
#driver = webdriver.Firefox(service = cService)

cService = webdriver.ChromeService(executable_path='/snap/bin/chromium.chromedriver')
driver = webdriver.Chrome(service = cService)
driver.get(url) 


time.sleep(random.randint(4, 7))
if(driver.current_url == url):
    page_source = driver.page_source

print(page_source)

soup = BeautifulSoup(page_source, 'html.parser')


print(soup)
print(soup.prettify())


#soup.find_all('table')

#soup.find("td")

soup.find('th').text.strip()


table = soup.find_all('table')[1]


table

#soup.find('table' , class_ = 'fullWidth')

#soup.find_all('th')

aircraft_titles = soup.find_all('th')


aircraft_table_title = [title.text for title in aircraft_titles]

print(aircraft_table_title)

aircraft_table_title = [title.text.strip() for title in aircraft_titles]

print(aircraft_table_title)

df = pd.DataFrame(columns = aircraft_table_title)


rows = table.find_all('tr')
rows

headers = [header.text.strip() for header in rows[1].find_all('th')]
headers = headers[1:]
headers


data = []
for row in rows[4:]:
    data.append([td.text.strip() for td in row.find_all('td')])
    
#columns = ['Flight', 'Aircraft', 'Origin', 'Destination', 'Departure', 'Estimated Arrival', 'Duration']


df = pd.DataFrame(data, columns=headers)

df[1:]


####################### Data Cleaning #################
df.rename(columns={'Ident': 'Aircraft_name'}, inplace=True)

df = df.to_csv('AircraftType27.csv', index=False)
