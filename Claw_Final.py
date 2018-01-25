# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 18:02:40 2018

@author: david
"""
import os
import shutil
import csv
import numpy as np
import requests
import urllib
from bs4 import BeautifulSoup

def html_file():
    url = 'https://www.yelp.com/search?find_loc=Austin,+TX&start={}0&cflt=restaurants'.format(i)   # Pass i into {} from 0(page 1) - 99(page 100)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}   # Unique user agent, avoid forbidden
    url_html = requests.get(url, headers=headers)
    soup = BeautifulSoup(url_html.text)   # Pass above text to the BeautifulSoup object, which returns a HTML-like data structure
    return soup

def img_claw(x):
    soup = html_file()
    
    i = 0
    for line in soup.findAll('a',{'class:','js-analytics-click'}): # line: <class 'bs4.element.Tag'>   
        soup1 = BeautifulSoup(str(line))
        if soup1.find('img') is not None:  # If key word 'img' exists
            i = i + 1
            if i > 2 and i < 13:   # In this html, 0 & 1 are repeated images, 13 - 32 are unrelated ones
                src = soup1.find('img').get('src')   # src is the img link
                print(src)
                response = urllib.request.urlopen(src)   # Open the link and read data
                img_bytes = response.read()
                x +=1   
                f = open('./claw_result'+'/' + str(x) + '.jpg', 'wb') # Open './demoimg/x.jpg' for writing in binary mode(wb)
                f.write(img_bytes)
                f.close()

def restaurant_claw():
    soup = html_file()
    
    i = 0
    for line in soup.findAll('a', {'class:', 'biz-name js-analytics-click'}): #soup.findAll('span', {'class:', 'indexed-biz-name'}):   #resaurant name 
        if line.string is not None: 
            if line.get('data-hovercard-id') is not None: 
                i +=1
                if 2<i and i<13:
                    print(line.string)
                    rest_name.append(line.string)
                    
    i = 0 #filter                                    
    for line in soup.select('div'): #rating, which is in the div type content
        #print(line)
        if line.get('class') is not None:
            #print(line.get('class')[0])
    
            if line.get('class')[0] == 'i-stars':
                i +=1
                #print(line)
                star = line.get('title').split()[0]   # split()分隔开str中字符，默认空格为分隔符
                if 2<i and i<13: 
                    rest_rating.append(star)
                    
    i = 0 #filter
    for line in soup.findAll('span',{'class:','review-count rating-qualifier'}):
        #print(line.string)
        i +=1
        if 2<i and i<13: 
            reviews_num.append(line.string.split()[0])
 
    i = 0
    for line in soup.findAll('span',{'class:','category-str-list'}):
        #print(line)
        i = i + 1
        if 2<i and i<13:
            soup1 = BeautifulSoup(str(line))
            y=[]
            for x in soup1.findAll('a'):
                y.append(x.string)
            food_type.append(','.join(y))    
    

               # ----------------------------- Main function -------------------------------------    

               
if __name__ == "__main__":
    rest_name = ['rest_name']
    rest_rating = ['rating']
    reviews_num = ['reviews_num']
    food_type = ['type']
    if os.path.exists('./claw_result'):   # If dir exists, remove it first
        shutil.rmtree('./claw_result')
    os.mkdir('./claw_result')   

    for i in range(100):      # Total pages to be clawed
        print('Page' + str(i + 1))
        restaurant_claw()
        img_claw(x = 10 * i)   # x is the unit digit for each img loop

    result = rest_name
    result = np.vstack((result, rest_rating))
    result = np.vstack((result, reviews_num))
    result = np.vstack((result, food_type))
    result = list(map(list, zip(*result)))   # Transpose list of lists: [[1,2],[3,4]] -> [[1,3],[2,4]];  for array, do A.T; for matrix, do zip(*A)

    with open('./claw_result/result.csv', 'w') as f: 
        wr = csv.writer(f, lineterminator='\n')        
        wr.writerows(result)   # For a flat list, use a loop .writerow(result[i])

    with open('./claw_result/result.txt', 'w') as f:   
        for i in range(len(rest_name)):   # List A: # of rows: len(A), # of columns: len(A[0])
            f.write(rest_name[i].center(30)+rest_rating[i].center(20)+\
                reviews_num[i].center(20)+food_type[i].strip().center(50)+'\n' )   # strip('x'):去除‘x’字符，默认为去除空格
         
             
