# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 14:51:56 2020

@author: sanman
"""
import urllib.request
import requests

from bs4 import BeautifulSoup
from datetime import date

## read the MF URL file
mfURLFile = open('MoneyControl_MF_List.txt', 'r') 
mfURLList = mfURLFile.readlines()
isHeaderFound = 0;

today = date.today()
date_dd_mm_yy = today.strftime("%d_%m_%Y")


fundname = 'stock'
final_distribution = open(fundname+"_ditribution_"+date_dd_mm_yy+".txt","w")
distribution_text=''

for mrURL in mfURLList:
    
    print(mrURL)
    
    mf_index = mrURL.find('mutual-funds/')+13
    portfolio_index = mrURL.find('/portfolio-holdings')
    print(mrURL[mf_index:portfolio_index])
    fund = mrURL[mf_index:portfolio_index]


    page = requests.get(mrURL);
    soup = BeautifulSoup(page.content,'html.parser')
    
    equityCompleteHoldingTable = soup.find_all(id='equityCompleteHoldingTable')[0]
    rows = equityCompleteHoldingTable.find_all('tr')
    
    
    for row in rows:
        distribution_row=''
       
        #pick headers
        if isHeaderFound == 0:
            headers = row.find_all('th')
            for header in headers:
                distribution_text=distribution_text+header.get_text()+'|'
            distribution_text = distribution_text+'funaname|date'+'\n'
            isHeaderFound = 1
            
        columns = row.find_all('td')
        col_count=1
        for col in columns:
            colValue=col.get_text()
            
            #if percentage then remove % sign
            if(col_count == 5):
                colValue=colValue.replace('%','')
            distribution_row = distribution_row+colValue.replace('\n', ' ').replace('\r', '')+'|'
            col_count = col_count+1
            if(colValue == '0.00%' or colValue == '0' or  colValue == '0.00'):
                distribution_row=''
                break
        
        if distribution_row != '':
            distribution_text=distribution_text+distribution_row+fund+'|'+today.strftime("%d-%m-%Y")+'\n'
    
final_distribution.write(distribution_text.replace(' ',''))
final_distribution.close()    
