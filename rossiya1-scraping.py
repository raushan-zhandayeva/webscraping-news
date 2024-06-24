#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 21:09:05 2024

@author: raushanzhandayeva
"""

# setting up 
from bs4 import BeautifulSoup #for parsing html
import os #for file manipulation
import pandas as pd #for data manipulation

#directory
new_directory = "/Users/raushanzhandayeva/Desktop/Dissertation/Rossiya-text/1. January 2022 - Ros 1" # change this to the directory where the HTML files are stored
os.chdir(new_directory)

# Initialize an empty list to store the data
data = [] 

# Loop through all the files in the directory
for filename in os.listdir(new_directory):
    if filename.endswith(".htm"):  # Check if the file has a .htm extension
    
        # Open the HTML file
        with open(filename, "r", encoding="windows-1251") as file:
            contents = file.read()

        # Parsing the HTML content
        soup = BeautifulSoup(contents, 'html.parser')

        # Finding the title
        headline = soup.find('title').text.strip()

        # Finding the date from the <meta> tag
        date_meta = soup.find('meta', attrs={'name': '_YR'})
        if date_meta:
            full_date = date_meta['content']
            date_published = full_date.split(' ')[0]  # Extract the date portion
        else:
            date_published = ''

        # Finding the text
        text_element = soup.find('p')
        if text_element:
            text = text_element.get_text(separator=' ').strip()
            # Remove the "Видеосюжет" parts using string manipulation
            text = text.split("Видеосюжет")[0].strip()
        else:
            text = ''

        # Remove the "Видеосюжет" parts using string manipulation
        text = text.split("Видеосюжет")[0].strip()

        # Append the extracted data to the list
        data.append({'Headline': headline, 'date_published': date_published, 'text': text})

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
df.to_excel("01_scraped_ros1_rus_jan22.xlsx", index=False) # change the name of the output file as needed (month)




