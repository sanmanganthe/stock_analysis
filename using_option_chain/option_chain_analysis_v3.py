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
import time

def wavg(group, avg_name, weight_name):
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()
    except TypeError:
        return d.mean()
        
stockListTech = ['AAPL','MSFT','GOOGL','VMW','FB']
stockListBank = ['BAC','JPM','V']
stockListRetail = ['AMZN','WMT','COST']
stockListTravel = ['DAL','SAVE']
stockListAuto = ['F','BA','GM','ABT','ABBV','JNJ','TSLA']
stockListIndex = ['XLK','TQQQ','XLF','DIV','VOO','NDAQ','DOW']
stockListTelecom = ['T','TMUS','ERIC','VZ']
stockListRE = ['CIM','O']
stockListEnt = ['DIS','NFLX']
stockListSmall = ['SPCE','NIO','BYND']
stockListChip = ['AMD','NVDA','INTC','QCOM','MU','AMAT']
stockListEnergy = ['VLO','XOM']
stockListTest= ['F']

stockList = stockListTech+stockListBank+stockListRetail+stockListEnergy
stockList2 = stockListIndex+stockListTelecom+stockListRE+stockListEnt
stockList3 = stockListTravel+stockListAuto+stockListSmall+stockListChip

months=3
nResults=20
requestCount=0

finalCompleteDF = pd.DataFrame()
stockType="Full_F"

slist = stockList+stockList2+stockList3
for stock in stockListTest:
    #time.sleep(60)
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
    try:
        stockPrice = si.get_live_price(stock)
        print(stockPrice)
        mainCallDF=pd.DataFrame()
        mainPutDF=pd.DataFrame()
        for i in range(months*4):
            expDate=d.strftime('%Y-%m-%d')
            #print(expDate)
            try:
                callDF = op.get_calls(stock,d)
                #requestCount = requestCount+1
                #print("Call Request Count "+str(requestCount))
                if not callDF.empty:
                    #print("Call options "+ str(callDF.size))
                    callDF['ExpiryDate']=expDate
                    callDF['OptionType']='CALL'
                    callDF['Count']=callDF.size
                    mainCallDF=mainCallDF.append(callDF)
                putDF = op.get_puts(stock,d)
                #requestCount = requestCount+1
                #print("put Request Count "+str(requestCount))
                if not putDF.empty:
                    #print("Put Options "+ str(putDF.size))
                    putDF['ExpiryDate']=expDate
                    putDF['OptionType']='PUT'
                    putDF['Count']=putDF.size
                    mainPutDF=mainPutDF.append(putDF)
            except:
                #print("Error Call options "+ str(callDF.size))
                #print("Error Put Options "+ str(putDF.size))
                pass
            finally:
                d += datetime.timedelta(7)
        print("Collected all data for "+stock+" datasize Calls-"+str(mainCallDF.size)+" Puts-"+str(mainPutDF.size))
        topNCallDF = pd.DataFrame()
        if not mainCallDF.empty:
            topNCallDF = mainCallDF.groupby(["ExpiryDate"]).apply(lambda x: x.sort_values(["Open Interest"], ascending = False)).reset_index(drop=True).groupby(["ExpiryDate"]).head(nResults)[['OptionType','Count','ExpiryDate','Strike','Open Interest']]
            #print(topNCallDF)
            #########################
            #callMeanDF = topNCallDF.groupby(["ExpiryDate"])['Strike'].mean();
            #print(callMeanDF)
            #########################'=
        if not mainPutDF.empty:
            topNPutDF = pd.DataFrame()
            topNPutDF = mainPutDF.groupby(["ExpiryDate"]).apply(lambda x: x.sort_values(["Open Interest"], ascending = False)).reset_index(drop=True).groupby(["ExpiryDate"]).head(nResults)[['OptionType','Count','ExpiryDate','Strike','Open Interest']]
            #print(topNPutDF)
            #########################
            #callMeanDF = topNCallDF.groupby(["ExpiryDate"])['Strike'].mean();
            #print(callMeanDF)
            #########################
        topNPutDF = topNPutDF.append(topNCallDF)
        #print(topNPutDF.size)
        if not topNPutDF.empty:
            topNPutDF.to_csv(stock+'_'+datetime.date.today().strftime('%Y-%m-%d')+".csv")
            wavgSet=topNPutDF.groupby("ExpiryDate").apply(wavg, "Strike", "Open Interest");
            #print("1")
            #print(putWavgSet)
            finalDF = pd.DataFrame()
            for index, value in wavgSet.items():
                finalDF = finalDF.append({'ExpiryDate': index, 'StrikePrice': value}, ignore_index=True)
            #print("2")
            finalDF['Stock']=stock
            finalDF['StockPrice']=stockPrice
            finalDF['PCR']=topNPutDF.size/topNCallDF.size
            #print("3")
            #print(finalDF.size)
            finalCompleteDF = finalCompleteDF.append(finalDF)
    except:
        print("Error with "+stock)
        pass
#########################
#mainCallDF.info()
print(finalCompleteDF)
finalCompleteDF.to_csv(stockType+'_'+datetime.date.today().strftime('%Y-%m-%d')+".csv")
#########################