#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:38:14 2023

@author: raushanzhandayeva
"""

#Loading packages
import os #to work with files
import zipfile #to work with .docx files
import xml.etree.ElementTree as ET #to parse XML content
import re #to work with regular expressions
import pandas as pd   #to work with dataframes
from tqdm import tqdm #to track the process
from datetime import datetime #to work with dates

#Open the folder with articles organized by month

folder_path = '/Users/raushanzhandayeva/Desktop/Dissertation/news/BBC_rus/DOCS/1_jan22' #change the path to the folder with articles
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
    my_text = " ".join(paragraph_texts)

    #now I need to clean 
    headline = my_text.split("BBC Russian")[0]
    headline = headline.strip(' ')
    headline

    date_published = my_text.split("Copyright")[0]
    date_published = date_published.split("Russian ")[1]
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
    date_published

    description = my_text.split("Highlight:")
    if len(description) > 1:
        description = my_text.split("Highlight:")[1]
        description = description.split("Body")[0]
        description = description.strip()
        description
    else: 
        description = "N/A"

    text = my_text.split("Body")[1]
    text = text.split("Graphic")[0]
    text = text.split("Classification")[0]
    text = text.split("Link to Image")
    text = " ".join(text)
    text = text.strip()
    text = text.strip(',') 
    text = text.strip(' ,')
    text

    tags = my_text.split("Subject:")
    if len(tags) > 1:
        # split by semicolon
        tags = my_text.split("Subject:")[1]
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
    else: 
        tags = "N/A"


    dataframe = {
        "date_published": [date_published],
        "headline": [headline],
        "description": [description],
        "text": [text],
        "tags": [tags]
        }

    df = pd.DataFrame(dataframe)
    return df

# Create an empty DataFrame to store the results
df_all = pd.DataFrame()

#scrape all articles in one file

for file in tqdm(files): #tqdm allows us to track the process
    df = scrape_article_nexi(file)
    df_all = pd.concat([df_all, df], ignore_index=True)

print(df_all)

df_all.to_excel('1_scraped_bbc_ru_jan22.xlsx', index=False) #save the results to an Excel file in the same folder, repeat for each month

#END
