
from selenium import webdriver

from Scrap_wp_functions import scrap_wiadomosci_wp, scrap_finanses_wp

from bs4 import BeautifulSoup

from io import StringIO
import boto3

import re
import pandas as pd

import time
import datetime




def write_time_to_bucket(act_time, string):
    
    save = act_time.strftime("%Y-%m-%d-%H:%M:%S")
    save = save + '.txt'
    
    with open(save, "a") as f:
        f.write(string + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + '\n')





chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

  

try:
    
    act_time = datetime.datetime.now()
    
    write_time_to_bucket(act_time, 'Initialize  ')
    
    driver = webdriver.Chrome("./chromedriver",chrome_options=chrome_options)

    url = 'https://www.wp.pl'

    driver.get(url)

    buts = driver.find_elements_by_tag_name("button")
    
    for but in buts:
        
        try:
            
            if " DO SERWISU" in but.text :
                but.click()
    
        except:
            pass
        
    
    write_time_to_bucket(act_time, 'After button click  ')
    
    #Convert to html
    
    html = driver.page_source
    soup = BeautifulSoup(html)
    
    write_time_to_bucket(act_time, 'Load page  ')
    
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
                                  'link': '', #b['href'],
                                  'text': b.text}, ignore_index=True)
    
    
    
    write_time_to_bucket(act_time, 'Mid step  ')
    
            
    wiadomosci = links[links.area == "Wiadomosci"]
            
    wiadomosci_wp = wiadomosci.link[wiadomosci.link.str.contains('wiadomosci.wp.pl')]        
            
    
    source_content = pd.DataFrame(columns = ['title', 'author', 'text',
                                             'comments', 'grades_pos', 'grades_neg',
                                             'wazne', 'smutne', 'ciekawe', 'irytujace'])
            
          
    output = pd.DataFrame() 
    
    ##print(time.clock() - t1)
    
    write_time_to_bucket(act_time, 'Finish 1st stage  ')
        
    for url in wiadomosci_wp:
        
        ##print(url)
        
        ##print(time.clock() - t1)
        
        
        if 'wiadomosci.wp.pl' in url:
            
            write_time_to_bucket(act_time, 'Wiadomosci st  ')
            
            t = scrap_wiadomosci_wp(driver, url)
            
            write_time_to_bucket(act_time, 'Wiadomosci stop  ')
            
            t = pd.DataFrame(t, index = [0])
            
            if output.shape[0] == 0:
                output = t
            else: 
                output = pd.concat([output, t], axis = 0, ignore_index = True)
            
        elif 'finanse.wp.pl' in url:
            
            write_time_to_bucket(act_time, 'Finanse.wp st  ')
            
            t = scrap_finanses_wp(driver, url)
            
            write_time_to_bucket(act_time, 'Finanse.wp stop  ')
            
            t = pd.DataFrame(t, index = [0])
            
            if output.shape[0] == 0:
                output = t
            else: 
                output = pd.concat([output, t], axis = 0, ignore_index = True)
            
    
    ##print(output)
    
    write_time_to_bucket(act_time, 'Finish all files  ')
    
    driver.quit()
    
    write_time_to_bucket(act_time, 'Save file  ')
    
    csv_buffer = StringIO()
    output.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    



    bucket = 'polish-internet'

    save_name = act_time.strftime("%Y-%m-%d-%H:%M:%S")
    folder_name = act_time.strftime("%Y-%m-%d")
    
    t = datetime.datetime.now()
    save_name2 = t.strftime("%Y-%m-%d-%H:%M:%S")

    save_name = 'test' + '/polish_net_wp_' + save_name + '_' + save_name2 + '.csv'

    s3_resource.Object(bucket, save_name).put(Body=csv_buffer.getvalue())
    
    write_time_to_bucket(act_time, 'Saved file  ')
    
except:
    driver.quit()
    





    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


