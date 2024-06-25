#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 20:38:36 2023

@author: raushanzhandayeva
"""
from bs4 import BeautifulSoup, SoupStrainer #for parsing html
import urllib.request as urllib2 #for downloading html
import re #for regular expressions
import requests #for downloading html
import pandas as pd #for data manipulation
from selenium import webdriver #for scraping javascript
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta #for date manipulation
import time #for time manipulation

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options) #initialize the webdriver

def get_links(url): #function to get links from the search page
    try:
        driver.get(url)    
        driver.maximize_window() 
        #driver.find_element_by_link_text('не интересуюсь').click() 
        print('No subscription') 
        
        start_time = time.time()  # Record the start time
        
        while True: 
            try: 
                print('Waiting for 10 seconds')  
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@role='button' and @title='Вперед']")))
            except TimeoutException: 
                break
            
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= 10:
                break  # Break the loop after 10 seconds
                
        html = driver.page_source 
        html = BeautifulSoup(html, "lxml") 
    
        articles = html.find_all('div', class_=re.compile(r'^media-block')) 
        
        if articles:
            links_list = [] 
            for article in articles:
                ankor = article.find('a', href=True)
           
                if ankor:
                    url = ankor['href']
                    url = 'https://www.currenttime.tv' + url 
                    links_list.append(url) 
                    
            links_df = pd.DataFrame({'links': links_list}) 
            links_df = links_df.drop_duplicates(subset='links', keep='last', inplace=False) 
    
            links_df.to_csv(filename, index=False)
    
            return links_df
    
    except NoSuchElementException:
        pass

    finally: # close the driver
        driver.quit()
        
urls = [] # List to store the URLs
for i in range(17, 79):  # Loop to generate the URLs
    i = str(i)
    link = "https://www.currenttime.tv/s?k=%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0&tab=all&pi=" + i + '&r=any&pp=50' # URL pattern
    urls.append(link)

# Printing the first few URLs for demonstration
print(urls[:5])

# Running the list 
for i in range(len(urls)):
    filename = f'links_{i+1}.csv'
    get_links(urls[i])

#END