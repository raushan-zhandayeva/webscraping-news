#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 13:21:11 2023

@author: raushanzhandayeva
"""

# conda install pandas requests bs4 selenium


from bs4 import BeautifulSoup, SoupStrainer #for parsing html
import urllib.request as urllib3 #for downloading html
import re #for regular expressions
import requests #for downloading html
import pandas as pd #for data manipulation
#from headers import HEADERS
from selenium import webdriver #for scraping javascript
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta #for date manipulation


driver = webdriver.Chrome("/Users/raushanzhandayeva/Library/CloudStorage/GoogleDrive-rzhandayeva@gwmail.gwu.edu/My Drive/ICPSR/Text Analysis/Project/chromedriver_mac64/chromedriver") #initialize the webdriver

def get_links(url): #function to get links from the search page
    
    try:
        driver.get(url)   
        driver.maximize_window() 
        try: 
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "Popup-telegram__close"))).click() #closing the telegram popup
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Подтвердить'))).click() #closing the cookies popup
            print('Closed cookies window')
        except NoSuchElementException:
            print("Popup or confirmation not found.")
        
        while True:
            try: 
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.LINK_TEXT, "Загрузить ещё"))) #waiting for the "Load more" button
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.find_element(By.LINK_TEXT, 'Загрузить ещё').click()
                print('Clicked on "Load more"')
            except TimeoutException:
                print('No more "Load more" buttons to click.') #if there are no more "Load more" buttons,
                break

        html = driver.page_source 
        html = BeautifulSoup(html, "lxml")  
        
        articles = html.find('div', {'class': 'listing__content listing__content_js'}) 
        ankor_list = articles.findChildren('a') 
        
        links_list = [] #empty list to store the links
        for ankor in ankor_list:
            url = ankor.get('href') 
            url = 'https://russian.rt.com' + url 
            
            if url not in links_list: 
                links_list.append(url) 
                # print(url) 
                
        links_df = pd.DataFrame({'links' : links_list }) 
        links_df = links_df.drop_duplicates(subset='links', keep='last', inplace=False) 
        links_df = links_df.drop(links_df.index[-1])  # getting rid of the incomplete url at the end
        
        links_df.to_csv(filename, index=False)
        
        return links_df
            
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally: 
        return links_df

     
# Defining the period I want to scrape 
start_date_str = "2023-08-01"
end_date_str = "2023-08-31"

# Convert the start and end dates to datetime objects
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

# Create an empty list to store the result
date_list = []

# Generate dates and append them to the list
current_date = start_date
while current_date <= end_date:
    date_list.append(current_date.strftime("%Y-%m-%d"))
    current_date += timedelta(days=1)
    
urls = []
 
for date in date_list:
   link = "https://russian.rt.com/search?q=%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0&type=News&df=" + date + "&dt=" + date # URL pattern
   urls.append(link)


# Running the list 
try: 
    for i in range(0, len(urls)):
        filename = f'links_{i+1}.csv'
        print(f"trying URL: {urls[i]}")
        get_links(urls[i])
    
finally:
    driver.quit()

#END