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
stock="BA"
months=1
nResults=20

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
print(si.get_live_price(stock))

#mainCallDF = op.get_calls(stock,d)
mainCallDF = op.get_calls(stock,d)
mainCallDF['ExpiryDate']=expDate
mainCallDF['OptionType']='CALL'
print(mainCallDF)
mainCallDF.info()


#mainPutDF = op.get_puts(stock,d)
mainPutDF = op.get_puts(stock,d)
mainPutDF['ExpiryDate']=d
mainPutDF['OptionType']='PUT'


for i in range(months*4):
    d += datetime.timedelta(7)
    expDate=d.strftime('%Y-%m-%d')
    print(expDate)
    try:
        callDF = op.get_calls(stock,d)
        print(callDF.count())
        callDF['ExpiryDate']=expDate
        callDF['OptionType']='CALL'
        mainCallDF=mainCallDF.append(callDF)
        putDF = op.get_puts(stock,d)
        print(putDF.count())
        putDF['ExpiryDate']=expDate
        putDF['OptionType']='PUT'
        mainPutDF=mainPutDF.append(putDF)
    except ValueError:
        pass
        #print("No option data for "+str(d))
        
topNCallDF = mainCallDF.groupby(["ExpiryDate"]).apply(lambda x: x.sort_values(["Open Interest"], ascending = False)).reset_index(drop=True).groupby(["ExpiryDate"]).head(nResults)[['OptionType','ExpiryDate','Strike','Open Interest']]
print(topNCallDF)
#########################
#callMeanDF = topNCallDF.groupby(["ExpiryDate"])['Strike'].mean();
#print(callMeanDF)
#########################

callWavgSet=topNCallDF.groupby("ExpiryDate").apply(wavg, "Strike", "Open Interest");
#print(callWavgSet)

cDF = pd.DataFrame()
for index, value in callWavgSet.items():
    cDF = cDF.append({'ExpiryDate': index, 'CallStrikePrice': value}, ignore_index=True)
#print(cDF)

topNPutDF = mainPutDF.groupby(["ExpiryDate"]).apply(lambda x: x.sort_values(["Open Interest"], ascending = False)).reset_index(drop=True).groupby(["ExpiryDate"]).head(nResults)[['OptionType','ExpiryDate','Strike','Open Interest']]
print(topNPutDF)
#########################
#callMeanDF = topNCallDF.groupby(["ExpiryDate"])['Strike'].mean();
#print(callMeanDF)
#########################

putWavgSet=topNPutDF.groupby("ExpiryDate").apply(wavg, "Strike", "Open Interest");
#print(putWavgSet)

pDF = pd.DataFrame()
for index, value in putWavgSet.items():
    pDF = pDF.append({'ExpiryDate': index, 'PutStrikePrice': value}, ignore_index=True)
#print(pDF)



putStrikePriceColumn = pDF["PutStrikePrice"]
finalOptionChain = pd.concat([cDF,putStrikePriceColumn], axis = 1)
print(finalOptionChain)


#########################
#mainCallDF.info()
finalOptionChain.to_csv(stock+'_'+str(months)+'months_prediction.csv')
#########################