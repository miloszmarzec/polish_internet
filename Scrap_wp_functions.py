import re
import pandas as pd
import time

from bs4 import BeautifulSoup

def scrap_oceny_wp(soup_tmp):
    
        
    comments = soup_tmp.find("div", {"class" : re.compile('gIyVIC4')})
    
    if not comments is None:
        comments = comments.text
    
    grades = soup_tmp.find("div", {"class" : re.compile('_1aAvOqM')})
    
    if not grades is None:
        grades =  grades.find_all("strong")
        
        grades_positive = grades[0].text
        grades_negative = grades[1].text
        
    else:
        grades_positive = ''
        grades_negative = ''
    
    others = soup_tmp.find("div", {"class" : re.compile('39tMEdf')})
    
    if not others is None:
        others = others.find_all("div", {"class" : re.compile('_1cYeTap')})
        
        others1 = others[0].text
        others2 = others[1].text
        others3 = others[2].text
        others4 = others[3].text
        
    else:
        others1 = ''
        others2 = ''
        others3 = ''
        others4 = ''
        
    output_grades = {'comments': comments,
                     'grades_pos': grades_positive,
                     'grades_neg': grades_negative,
                     'wazne': others1, 
                     'smutne': others2, 
                     'ciekawe': others3, 
                     'irytujace': others4}
    
    return output_grades
    
    
def wait_till_komentarze_loaded(driver):
    
    num_comments = '0komentarze'
    
    t1 = time.clock()
    
    while (num_comments == '0komentarze'):
        
        html = driver.page_source
        soup_tmp = BeautifulSoup(html) 
    
        comments = soup_tmp.find("div", {"class" : re.compile('gIyVIC4')})
    
        if not comments is None:
            num_comments = comments.text
        else:
            num_comments = None
            
        #print(num_comments)
        
    t2 = time.clock()
    
    #print(t2 - t1)


def scrap_wiadomosci_wp(driver, url):
    
    t1 = time.clock()
    
    driver.get(url)  
    
    #print(time.clock() - t1)
    
    wait_till_komentarze_loaded(driver)
    
    #print(time.clock() - t1)

    
    html = driver.page_source
    soup_tmp = BeautifulSoup(html) 
    
    #print(soup_tmp)
    
    paragraphs = soup_tmp.find('article')
   
    art_class = paragraphs['class']
    

    try:
        author_article = paragraphs.find("span", {"class" : re.compile('author*')})
                         
        if len(author_article) != 0:
            author_article = author_article.text
    except:
        author_article = ''
        
    try:              
        if art_class[0] == 'gallery':
            title_article = [x.get_text() for x in paragraphs.find_all(re.compile(r"^h\d$"))]
                             
        else:
            title_article = paragraphs.findAll("h1", {"class" : re.compile('article-.*')})
             
            if len(title_article) != 0:
                title_article = title_article[0].text     
                
    except:
        title_article = ''
                         
    try:
        text_article = paragraphs.findAll("div", {"class" : re.compile('article-.*')})
        text_article = [row.text for row in text_article]
        
        text_article = ''.join(text_article)
    except:
        text_article = ''
    
    #print(time.clock() - t1)
    
    output_grades = scrap_oceny_wp(soup_tmp)

    #print(time.clock() - t1)
    
    output = {'title' : title_article, 
              'author': author_article,
              'text': text_article}
    
    output.update(output_grades)
    
    return output
    


def scrap_finanses_wp(driver, url):
    
    t1 = time.clock()
    
    driver.get(url)  
    
    #print(time.clock() - t1)
    
    wait_till_komentarze_loaded(driver)
    
    #print(time.clock() - t1)
    
    html = driver.page_source
    soup_tmp = BeautifulSoup(html) 
    
    
    
    tmp = soup_tmp.find("article")

    tmp1 = tmp.find("div", {"data-st-area" : 'article-header'})
    
    tmp1_author = tmp.find("span", {"itemprop" : 'name'}).text
    
    tmp1_title = tmp.find("h1", {"class" : 'article--title'}).text
    
    
    tmp2 = tmp.find_all("div", {"class" : re.compile('article--*')})
    
    tmp2 = [t2.text for t2 in tmp2]
    
    tmp2 = ''.join(tmp2)
    
    #print(tmp1_author)
    #print(tmp1_title)
    
    #print(time.clock() - t1)
    
    output_grades = scrap_oceny_wp(soup_tmp)
    
    #print(time.clock() - t1)
    
    output = {'title' : tmp1_title, 
              'author': tmp1_author,
              'text': tmp2}
    
    output.update(output_grades)
    
    return output
    
    
    
    