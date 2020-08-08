# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 00:26:09 2020

@author: sanman
"""

import urllib.request
import requests

from bs4 import BeautifulSoup

fundname='aditya-birla-sun-life-equity-fund'
fundcode='MAC006'

fundname='baroda-pioneer-multi-cap-fund-direct-plan-b'
fundcode='MBO088'

fundname='canara-robeco-blue-chip-equity-fund-direct-plan'
fundcode='MCA212'

link='https://www.moneycontrol.com/mutual-funds/'+fundname+'/portfolio-holdings/'+fundcode
#link='https://www.moneycontrol.com/mutual-funds/baroda-pioneer-multi-cap-fund-direct-plan-b/portfolio-overview/MBO088'
#link='https://www.google.com'

mf_index = link.find('mutual-funds/')+13
portfolio_index = link.find('/portfolio-holdings')
print(link[mf_index:portfolio_index])


#### USING URLLIB

#headers = {}
#headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
#req = urllib.request.Request(link, headers = headers)
#html = urllib.request.urlopen(req).read()
#print(el)
#print(html)

#### USING REQUESTS
page = requests.get(link);
#print(page.text)
#print(page.apparent_encoding)
#print(page.encoding)
#print(page.headers)
#print(page.content.decode('UTF-8'))
#import json
#print(json.loads(page.text))

fname="originalHTML.txt"
with open(fname, "w", encoding="utf-8") as f:
    f.write(page.text)
    
soup = BeautifulSoup(page.content,'html.parser')
#subText = soup.find_all(class_='robo_medium')

file_subHTML = open(fundname+"_subHTML.txt","w")
final_distribution = open(fundname+"_ditribution.txt","w")
equityCompleteHoldingTable = soup.find_all(id='equityCompleteHoldingTable')[0]
rows = equityCompleteHoldingTable.find_all('tr')

distribution_text=''

for row in rows:
    distribution_row=''
    file_subHTML.write(str(row))
    
    #pick headers
    headers = row.find_all('th')
    for header in headers:
        distribution_text=distribution_text+header.get_text()+'|'
        
    columns = row.find_all('td')
    for col in columns:
        colValue=col.get_text()
        distribution_row = distribution_row+colValue.replace('\n', ' ').replace('\r', '')+'|'
        if(colValue == '0.00%' or colValue == '0'):
            distribution_row=''
            break
            
    distribution_text=distribution_text+distribution_row+'\n'

final_distribution.write(distribution_text.replace(' ',''))
final_distribution.close()    
file_subHTML.close()

## write to file
#file_handle = open("html.txt","a")
#file_handle.write("text")
#file_handle.close()