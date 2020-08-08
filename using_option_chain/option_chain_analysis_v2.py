# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 22:51:07 2020

@author: sanman
"""

from yahoo_fin import stock_info as si
from yahoo_fin import options as op
import datetime
import numpy as np
import pandas as pd

def wavg(group, avg_name, weight_name):
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()
    except TypeError:
        return d.mean()
#AAPL
#TSLA
#F
#MSFT
#AMZN
stockList = ['AAPL','AMZN','MSFT','F','TQQQ','TSLA','BAC','JPM','ABT','CIM','VMW','V','WMT','XLK','XLF','GOOGL','T','INTC','FB','COST','ERIC','DAL','SAVE','BA','TMUS','NVDA']
months=6
nResults=30

finalCompleteDF = pd.DataFrame()

for stock in stockList:
    print(stock)
    #########################
    #latestPriceDF = si.get_live_price(stock)
    #print(latestPriceDF)
    
    #financialsDF = si.get_financials(stock)
    #print(financialsDF)
    #########################
    d = datetime.date.today()
    #monday==0
    while d.weekday() != 4:
        d += datetime.timedelta(1)
    expDate=d.strftime('%Y-%m-%d')
    #mainCallDF = op.get_calls(stock,d)
    mainCallDF = op.get_calls(stock,d)
    mainCallDF['ExpiryDate']=expDate
    mainCallDF['OptionType']='CALL'
    #mainPutDF = op.get_puts(stock,d)
    mainPutDF = op.get_puts(stock,d)
    mainPutDF['ExpiryDate']=expDate
    mainPutDF['OptionType']='PUT'
    for i in range(months*4):
        d += datetime.timedelta(7)
        expDate=d.strftime('%Y-%m-%d')
        try:
            callDF = op.get_calls(stock,d)
            callDF['ExpiryDate']=expDate
            callDF['OptionType']='CALL'
            mainCallDF=mainCallDF.append(callDF)
            putDF = op.get_puts(stock,d)
            putDF['ExpiryDate']=expDate
            putDF['OptionType']='PUT'
            mainPutDF=mainPutDF.append(putDF)
        except ValueError:
            pass
            #print("No option data for "+str(d))
    topNCallDF = mainCallDF.groupby(["ExpiryDate"]).apply(lambda x: x.sort_values(["Open Interest"], ascending = False)).reset_index(drop=True).groupby(["ExpiryDate"]).head(nResults)[['OptionType','ExpiryDate','Strike','Open Interest']]
    #print(topNCallDF)
    #########################
    #callMeanDF = topNCallDF.groupby(["ExpiryDate"])['Strike'].mean();
    #print(callMeanDF)
    #########################
    topNPutDF = mainPutDF.groupby(["ExpiryDate"]).apply(lambda x: x.sort_values(["Open Interest"], ascending = False)).reset_index(drop=True).groupby(["ExpiryDate"]).head(nResults)[['OptionType','ExpiryDate','Strike','Open Interest']]
    #print(topNPutDF)
    #########################
    #callMeanDF = topNCallDF.groupby(["ExpiryDate"])['Strike'].mean();
    #print(callMeanDF)
    #########################
    topNPutDF = topNPutDF.append(topNCallDF)
    wavgSet=topNPutDF.groupby("ExpiryDate").apply(wavg, "Strike", "Open Interest");
    #print(putWavgSet)
    finalDF = pd.DataFrame()
    for index, value in wavgSet.items():
        finalDF = finalDF.append({'ExpiryDate': index, 'StrikePrice': value}, ignore_index=True)
    finalDF['Stock']=stock
    finalCompleteDF = finalCompleteDF.append(finalDF)
#########################
#mainCallDF.info()
print(finalCompleteDF)
finalCompleteDF.to_csv('Prediction.csv')
#########################