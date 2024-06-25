#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:03:46 2023

@author: raushanzhandayeva
"""

from bs4 import BeautifulSoup, SoupStrainer #for parsing html
import urllib.request as urllib3 #for downloading html
import re #for regular expressions
import requests #for downloading html
import pandas as pd #for data manipulation
#from headers import HEADERS
from selenium import webdriver #for scraping javascript
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta #for date manipulation
import time #for time manipulation

driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver") #initialize the webdriver

def get_links(url,file):  #function to get links from the search page
    try:
        driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver") 
        driver.get(url)    
        driver.maximize_window() 
        #driver.find_element_by_link_text('не интересуюсь').click() 
        print('No subscription') 
        
        start_time = time.time()  # Record the start time
        
        while True: 
            try: 
                print('Waiting for 10 seconds')  
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@role='button' and @title='Следующий']"))) #waiting for the "Next" button
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
                    url = 'https://www.svoboda.org' + url 
                    links_list.append(url) 
                    
            links_df = pd.DataFrame({'links': links_list}) 
            links_df = links_df.drop_duplicates(subset='links', keep='last', inplace=False) 
    
            links_df.to_csv(filename, index=False)
    
            return links_df
    
    except NoSuchElementException:
        pass

    finally: 
        driver.quit()
        

urls = [] #empty list to store the urls
for i in range(227, 243): 
    link = "https://www.svoboda.org/s?k=%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0&tab=news&pi=" + str(i) + '&r=any&pp=50' # URL pattern
    urls.append(link)


# Printing the first few URLs for demonstration
print(urls[:5])

# Running the list 
for i in range(len(urls)):
    filename = f'links_addition{i+1}.csv'
    get_links(urls[i], filename)



#END
