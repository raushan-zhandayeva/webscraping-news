#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 15:13:40 2023

@author: raushanzhandayeva
"""

#This is more important though - actual text 
import os #to work with files
import zipfile #to work with .docx files
import xml.etree.ElementTree as ET #to parse XML content
import re #to work with regular expressions
import pandas as pd #to work with dataframes
from tqdm import tqdm #to track the process
from datetime import datetime #to work with dates

#Open the folder with articles organized by month

folder_path = "/Users/raushanzhandayeva/Desktop/Dissertation/news/EURO_rus/DOCS/1_jan23"  #change the path to the folder with articles
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and (f.endswith('.docx') or f.endswith('.doc'))]

def scrape_article_nexi(file):
    file_path = os.path.join(folder_path, file)
    try:
      #Open .docx file as a zip file.
      with zipfile.ZipFile(file_path, 'r') as docx_file:
          # Extract document.xml file from the .docx file.
          document_xml = docx_file.read('word/document.xml')

    except zipfile.BadZipFile:
         print(f"Could not open {file_path} as a zip file.")
         return None
  
    # Parse the XML content.
    root = ET.fromstring(document_xml)

    # Define Word document namespace
    namespaces = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Find all paragraph elements.
    paragraphs = root.findall('.//w:p', namespaces)

    # Extract and store the text of each paragraph in a list.
    paragraph_texts = []
    for paragraph in paragraphs:
        texts = paragraph.findall('.//w:t', namespaces)
        paragraph_text = ' '.join(text.text for text in texts if text.text)
        paragraph_texts.append(paragraph_text)

    # Now 'paragraph_texts' is a list of the text of each paragraph.
    print(paragraph_texts)
    my_text = ", ".join(paragraph_texts)

    #Now I need to clean 
    headline = my_text.split("EuroNews - Russian Version")[0]
    headline = headline.strip(' ,')
    headline

    date_published = my_text.split("Copyright")[0]
    date_published = date_published.split("Version, ")[1]
    date_published
    def extract_date(string):
        # Regular expression pattern to match the date format
        pattern = r'[A-Za-z]+ \d{1,2}, \d{4}'
        # Search for the pattern in the string
        match = re.search(pattern, string)
        if match:
            return match.group()
        return None 
    date_published = extract_date(date_published)
    date_published = datetime.strptime(date_published, "%B %d, %Y").date()

    description = my_text.split("Highlight:")[1]
    description = description.split(", Body")[0]
    description = description.replace('\xa0', '')
    description = description.strip()
    description

    text = my_text.split("Body")[1]
    text = text.split("Classification")[0]
    text = text.strip()
    text = text.strip(',') 
    text = text.strip(' ,')
    text = text.replace('\xa0', '')
    text

    tags = my_text.split("Subject:")[1]
    # split by semicolon
    parts = tags.split(';')
    tags_list = []
    # now parts is a list of substrings
    for part in parts:
        # split by spaces and take the first part
        substring = part.split(' (')[0].strip()
        tags_list.append(substring)
        print(tags_list)   
    tags = [tags_list.replace('\xa0', '') for tags_list in tags_list]
    tags = ", ".join(tags)

    dataframe = {
        "date_published": [date_published],
        "headline": [headline],
        "description": [description],
        "text": [text],
        "tags": [tags]
        }

    df = pd.DataFrame(dataframe)
    return df


#Create an empty DataFrame to store the results
df_all = pd.DataFrame()

#scrape all articles in one file

for file in tqdm(files): #tqdm allows us to track the process
    df = scrape_article_nexi(file)
    df_all = pd.concat([df_all, df], ignore_index=True)

print(df_all)

df_all.to_excel('01_scraped_euro_ru_dec23.xlsx', index=False) #save the results to an Excel file in the same folder, repeat for each month


#END





