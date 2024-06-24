# Webscraping News: Russia-Ukraine War Media Analysis

## Project Overview 

This repository is a part of the large research project aimed at collecting, tracking, and understanding diverse media narratives surrounding the Russia-Ukraine war. The war serves as a stark illustration of competing narratives, and media outlets affiliated with different actors striving to shape public understanding of the events and garner international support. While acknowledging the existence of various competing narratives across the globe and the narrative availability is not binary in nature, my analysis predominantly categorizes them into two primary streams, namely pro-Russian and pro-Western (or pro-Ukrainian) narratives.

## Data Collection 

I employed advanced web scraping techniques to gather news articles containing the query "Ukraine" (or "Ukrain*") from January 2022 to December 2023. The data collection process encompassed both Russian and Western news sources to ensure a balanced representation of narratives. The following table presents an overview of the scraped sources and their respective article counts. Across 7 sources, I have collected 125,428 documents. 

| Source        | Orientation        | Number of Articles/News |
| ------------- | ------------- | ------------- |
| Russia Today  | pro-Russia    | 61,969        |
| Channel 1     | pro-Russia    | 12,683        |
| Rossiya 1     | pro-Russia    | 10,479        |  
| Euronews      | pro-Ukraine   | 4,888         |
| Radio Liberty | pro-Ukraine   | 14,667        |
| Current Time  | pro-Ukraine   | 16,877        |
| BBC           | pro-Ukraine   | 3,865         |

The data extraction process was implemented using Python, leveraging Selenium (useful for dynamic content rendering and interaction with web elements) and BeautifulSoup (for parsing HTML and XML documents to extract relevant information) libraries. Post-extraction data cleaning and formatting were performed using R, ensuring consistency and preparing the dataset for further analysis.
