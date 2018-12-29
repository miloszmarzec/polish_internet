from selenium import webdriver
from bs4 import BeautifulSoup

import re
import pandas as pd

import time

#Load page and click GDPR pop up

url = 'https://www.wp.pl'

driver = webdriver.Firefox(executable_path=r'C:\Users\Witek\Desktop\geckodriver.exe')
driver.get(url)


buts = driver.find_elements_by_tag_name("button")

for but in buts:
    
    try:
        
        if but.text == "PRZECHODZĘ DO SERWISU":
            but.click()

    except:
        pass


#Convert to html

html = driver.page_source
soup = BeautifulSoup(html)

divs = soup.find_all('div')
   
tmp = soup.find("div", {"id": "glonews"})

blocks = tmp.find_all("div", {"data-st-area": "Wiadomosci"})

links = pd.DataFrame(columns = ['area', 'link', 'text'])

for b in blocks:
    
    sub_block = b.find_all('a')
    
    for sb in sub_block:
        
        links = links.append({'area': 'Wiadomosci', 
                              'link': sb['href'],
                              'text': sb.text}, ignore_index=True)


other_blocks = ["Glonews-glowny", "belka-opinions", "Glonews-high",
                "Glonews-low", "Wpisy-tv"]

for ob in other_blocks:
    blocks = tmp.find_all("a", {"data-st-area": ob})
    
    for b in blocks:
        
        links = links.append({'area': ob, 
                              'link': b['href'],
                              'text': b.text}, ignore_index=True)





        
wiadomosci = links[links.area == "Wiadomosci"]
        
wiadomosci_wp = wiadomosci.link[wiadomosci.link.str.contains('wiadomosci.wp.pl')]        
        

source_content = pd.DataFrame(columns = ['title', 'author', 'text',
                                         'comments', 'grades_pos', 'grades_neg',
                                         'wazne', 'smutne', 'ciekawe', 'irytujace'])
        
      
for url in wiadomosci_wp:
    
    
    if url.str.contains('wiadomosci.wp.pl'):
        scrap_wiadomosci_wp(driver, url)
        
    else if url.str.contains('finanse.wp.pl'):
        t = scrap_finanses_wp(driver, url)
        
        
# co gdy temat to tv?


