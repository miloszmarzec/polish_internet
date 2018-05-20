# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 22:29:10 2018
@author: Witek
Webscrap from wirtualna polska WP.PL
"""


"""
Right now I am interested in main news.
Main news are in glonews area which is splitted into:
1) belka-opinions
2) Glonews-glowny
3) Glonews-gorna-mozaika
4) Wiadomosci
5) Wpisy-tv
"""

"""
\xa0 is actually non-breaking space in Latin1 (ISO 8859-1), also chr(160). 
You should replace it with a space.

string = string.replace(u'\xa0', u' ')
"""

from bs4 import BeautifulSoup

import requests
import re

url = "wp.pl"

r  = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data)


divs = soup.find_all('div')


#Bottom area is generated using JS so right now I only take top area 
for d in divs:
    
    if d.get('data-st-area') is not None:
        
        print(d.get('data-st-area'))
        
        classes = d.find_all('a')
        
        for cl in classes:
            link = cl.get('href')
            text = cl.text
            
            print([link, text])
            
        print('---------------------')
        
        

important_areas = ['Glonews', 'Glonews-glowny', 
                   'Glonews-gorna-mozaika', 
                   'Wiadomosci', 'Wpisy-tv']

import pandas as pd

container = pd.DataFrame(columns= ["area", "title", "link"])
container_content = pd.DataFrame(columns= ["area", "title", "link", "class", "author", "title", "site"])
        
for d in divs:
    
    if d.get('data-st-area') in important_areas:
        
        print(d.get('data-st-area'))
        
        classes = d.find_all('a')
        
        for cl in classes:
            link = cl.get('href')
            text = cl.text
            
            print(d.get('data-st-area'))
            print(link)
            print(text)
            
            r_tmp  = requests.get(link)
            data_tmp = r_tmp.text
            soup_tmp = BeautifulSoup(data_tmp, "html.parser") 
             
            
            paragraphs = soup_tmp.find('article')
            
            container.loc[container.shape[0]] = [d.get('data-st-area'), text, link]
            
            if d.get('data-st-area') == 'Glonews':
                
                if "www.money.pl" in link:
                    
                    author_article = paragraphs.findAll('div', {'class': 'author-name'})[0].text
                    title_article = paragraphs.findAll('h1', {'class': 'article__title'})[0].text
                    
                    text_article = paragraphs.findAll('p')
                    text_article = [row.text for row in text_article]
                    
                    tmp = [d.get('data-st-area'), text, link, art_class,
                           author_article, title_article, text_article]
                    
                else:
                
                    try:
                        art_class = paragraphs['class']
                    except:
                        art_class = []    
                    
                    try:
                    
                        author_article = paragraphs.findAll("span", {"class" : re.compile('author-name*')})
                        
                        if len(author_article) != 0:
                            author_article = author_article[0].text
                        
                        if art_class[0] == 'gallery':
                            title_article = [x.get_text() for x in paragraphs.find_all(re.compile(r"^h\d$"))]
                            
                        else:
                            title_article = paragraphs.findAll("h1", {"class" : re.compile('article-.*')})
                        
                            if len(title_article) != 0:
                                title_article = title_article[0].text          
                        
                        print([author_article, title_article])
                        
                        text_article = paragraphs.findAll("div", {"class" : re.compile('article-.*')})
                        text_article = [row.text for row in text_article]
        
                        tmp = [d.get('data-st-area'), text, link, art_class,
                               author_article, title_article, text_article]
        
                    except:
                        tmp = [d.get('data-st-area'), text, link, art_class,
                               "error", "error", "error"]
                    
                container_content.loc[container_content.shape[0]] = tmp
                    
            
        print('---------------------')      
        






