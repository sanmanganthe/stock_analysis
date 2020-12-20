# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 00:26:09 2020

@author: sanman
"""

import requests
from datetime import date

from bs4 import BeautifulSoup

link='https://mutualfunds.com/funds/mmgpx-morgan-stanley-vif-discovery-i/#holdings-anchor'

mfURLFile = open('MF_List.txt', 'r') 
mfURLList = mfURLFile.readlines()

    
today = date.today()
date_dd_mm_yy = today.strftime("%d_%m_%Y")
final_distribution = open("ditribution_"+date_dd_mm_yy+".txt","w")
distribution_text='Type,Stock,Distribution\n'

for link in mfURLList:
   
    page = requests.get(link);
    soup = BeautifulSoup(page.content,'html.parser')
    
    MFtypeLi = soup.find_all('li',{'class' : 'n-text__display_sm t-font-semibold lg:t-text-lg lg:t-leading-normal lg:t-font-semibold t-underline hover:t-text-blue-550'})[0]
    MFTypeA = MFtypeLi.find_all('a')[0]
    MTType = MFTypeA.get_text()
    
    col = 1
    
    for li in soup.find_all('li',{'class' : 'n-text__display_sm t-p-3 even:t-bg-white odd:t-bg-gray-65'}):
        for span in li.find_all('span'):
            val = span.get_text().replace('%','')    
            if(col == 1):
                distribution_text = distribution_text + MTType +','+ val +','
                col=col+1
            else:   
                distribution_text = distribution_text + val +'\n'
                col=1

print(distribution_text)
final_distribution.write(distribution_text)
final_distribution.close() 