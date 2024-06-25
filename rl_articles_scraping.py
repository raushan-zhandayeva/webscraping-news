# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests #for downloading html
from bs4 import BeautifulSoup #for parsing html
import pandas as pd #for data manipulation
from tqdm import tqdm #for tracking the process
from datetime import datetime #for date manipulation
import time #for pausing the process

url = "https://www.svoboda.org/a/s-24-fevralya-2022-goda-rossiyane-osnovali-v-gruzii-21-tysyachu-kompaniy/32518388.html" #url of the article
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# Headline
headline = soup.title.string

#Date published
date_element = soup.find_all("time", attrs={"pubdate":True})[0]
date_string = date_element['datetime']
date = date_string.split("T")[0]

# Description
description_element = soup.find_all("meta", attrs={"name":"description"})[0]
description = description_element.get('content')

# Text
text_element = soup.find_all(class_="wsw")[0]
for p in text_element.find_all('p', class_='ta-c'):
    p.decompose()
for em in text_element.find_all('em'):
    em.decompose()
text_element = text_element.find_all('p')
extracted_text = "\n".join(p.get_text() for p in text_element)
text = extracted_text.replace('\n', '')


urls_df = pd.read_csv('lib_rus_links_jan22_feb22.csv')  #load the csv file with links (change the name depending on the month)
urls = urls_df["links"].tolist() 

def scrape_article(url):
    try:
        r = requests.get(url)
    
        # Check if the request was successful (status code 200)
        if r.status_code != 200:
            print(f"Error: Request failed with status code {r.status_code}")
            return None
    
        soup = BeautifulSoup(r.text, 'html.parser')

        # Headline
        headline = soup.title.string
        
        #Date published
        date_element = soup.find_all("time", attrs={"pubdate":True})[0]
        date_string = date_element['datetime']
        date = date_string.split("T")[0]

        # Description
        description_element = soup.find_all("meta", attrs={"name":"description"})[0]
        description = description_element.get('content')

        # Text
        text_element = soup.find_all(class_="wsw")[0]
        for p in text_element.find_all('p', class_='ta-c'):
            p.decompose()
        for em in text_element.find_all('em'):
            em.decompose()
        text_element = text_element.find_all('p')
        extracted_text = "\n".join(p.get_text() for p in text_element)
        text = extracted_text.replace('\n', '')
        
        dataframe = {
            "link": [url],
            "date_published": [date],
            "headline": [headline],
            "description": [description],
            "text": [text]
        }
        
        
        df = pd.DataFrame(dataframe)

        return df

    except Exception as e:
        print(f"Error occurred while scraping: {e}")
        error_dataframe = {
            "link": [url],
            "date_published": ["N/A"],
            "headline": ["N/A"],
            "description": ["N/A"],
            "text": ["N/A"]
            }
    return pd.DataFrame(error_dataframe)

# Create an empty DataFrame to store the results
df_all = pd.DataFrame()

for idx, url in enumerate(tqdm(urls)): # tqdm allows us to track the process
    if idx % 50 == 0 and idx != 0: # Check if index is divisible by 50, excluding the first index
        time.sleep(60)
        df = scrape_article(url)
        df_all = pd.concat([df_all, df], ignore_index=True)
    else: 
        df = scrape_article(url)
        df_all = pd.concat([df_all, df], ignore_index=True)

print(df_all)

df_all.to_excel('scraped_liberty_jan22_feb22.xlsx', index=False) #save the results to an excel file
    

#END