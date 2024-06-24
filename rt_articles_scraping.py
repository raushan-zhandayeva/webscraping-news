#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 17:05:50 2023

@author: raushanzhandayeva
"""

import requests #for downloading html
from bs4 import BeautifulSoup #for parsing html
import pandas as pd #for data manipulation
from tqdm import tqdm #for tracking the process
from datetime import datetime #for date manipulation

urls_df = pd.read_csv('01_jan23.csv') #load the csv file with links (change the name depending on the month)
urls = urls_df["links"].tolist()

def scrape_article(url): #function to scrape the article
    try:
        r = requests.get(url)
    
        # Check if the request was successful (status code 200)
        if r.status_code != 200:
            print(f"Error: Request failed with status code {r.status_code}")
            return None
    
        soup = BeautifulSoup(r.text, 'html.parser')
    
        # Headline
        headline = soup.title.string
    
        # Date published
        date_element = soup.find_all(class_="date")
        if len(date_element) == 0:
            date_element = soup.find_all(class_="Timestamp-root Timestamp-defautl")[0]
            date_element = date_element.text
            date = date_element.split(",")[0]
            date = date.strip()
            date
        else:
            date_element = soup.find_all(class_="date")[0]
            date = date_element.text
            date = date.split(",")[0]
            date = date.strip()
            date 

            month_translation = {
            'января': 'January',
            'февраля': 'February',
            'марта': 'March',
            'апреля': 'April',
            'мая': 'May',
            'июня': 'June',
            'июля': 'July',
            'августа': 'August',
            'сентября': 'September',
            'октября': 'October',
            'ноября': 'November',
            'декабря': 'December'
                  }

            parts = date.split()
            # Translate the month to English
            parts[1] = month_translation[parts[1]]
            # Reconstruct the date string in the format 'dd month yyyy'
            date = f'{parts[0]} {parts[1]} {parts[2]}'
            # Convert to a datetime object 
            date = datetime.strptime(date,'%d %B %Y')
            date = date.strftime('%Y-%m-%d')
        
    
        # Description
        description_element = soup.find_all("meta", attrs={"name":"description"})[0]
        description = description_element.get('content')
      
        # Text
        if soup.find(class_="text"):
            text_element = soup.find(class_="text")
        elif soup.find(class_='article__text article__text_article-page js-mediator-article'):
            text_element = soup.find(class_='article__text article__text_article-page js-mediator-article')
        else:
            text_element = soup.find(class_="ArticleView-text")

        embeds = text_element.find_all('div', class_='rtcode')
        for embed in embeds:
            embed.extract()
        text = text_element.get_text().strip()
        
        # Tags
        tags = soup.find_all(class_="tags-trends__link link link_underline_color")

        all_tags = []
        for i in range(0, len(tags)):
            tag = tags[i].text
            tag = tag.strip()
            all_tags.append(tag)
        all_tags
        
        dataframe = {
            "link": [url],
            "date_published": [date],
            "headline": [headline],
            "description": [description],
            "text": [text],
            "tags": [all_tags]
        }
        
        
        df = pd.DataFrame(dataframe)
        df['tags'] = df['tags'].apply(', '.join)

        return df

    except Exception as e:
        print(f"Error occurred while scraping: {e}")
        error_dataframe = {
            "link": [url],
            "date_published": ["N/A"],
            "headline": ["N/A"],
            "description": ["N/A"],
            "text": ["N/A"],
            "tags": [""]
        }
        return pd.DataFrame(error_dataframe)

# Create an empty DataFrame to store the results
df_all = pd.DataFrame()

for url in tqdm(urls): #tqdm allows us to track the process
    df = scrape_article(url)
    df_all = pd.concat([df_all, df], ignore_index=True)

print(df_all)

df_all.to_excel('01_scraped_rt_rus_jan23.xlsx', index=False) #save the data to an excel file (change the name depending on the month)


        
    





