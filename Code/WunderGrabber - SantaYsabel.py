# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 15:58:56 2016

@author: alex.messina
"""

import urllib2
import datetime
from BeautifulSoup import BeautifulSoup
from pandas import DataFrame, to_datetime, date_range
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import requests

## Grabs weather data from a WeatherUnderground station 
## https://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=MSYRSD&day=18&month=10&year=2016&graphspan=day&format=1
datagrab = True

## Station ID
site = 'KCARAMON70' ##stations needed

## Start date
startdatetime= '20161017 00:00:00'
## End date
now = datetime.datetime.now()
daterange = date_range(startdatetime,now,freq='D')

## Enter URL

## Data columns
## write header columns in empty DataFrame
columns = ['Time','TemperatureF','DewpointF','PressureIn','WindDirection','WindDirectionDegrees','WindSpeedMPH','WindSpeedGustMPH','Humidity','HourlyPrecipIn','Conditions','Clouds','dailyrainin','SoftwareType','DateUTC']

df = pd.DataFrame()#columns=columns)

if datagrab == True:
    print 'Grabbing data for site: '+site+'...'
    print '...from date range: '+str(daterange[0])+' to '+str(daterange[-1])
    for date in daterange:
        if date < now:
            print date
            try:
                ##enter web address of data
                url = 'https://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID='+site+'&day='+str(date.day)+'&month='+str(date.month)+'&year='+str(date.year)+'&graphspan=day&format=1'
                print url
                ## Get data from website
                s = requests.get(url).content.split('\n')
                ## Iterate through and filter data
                for line in s:
                    if line != '<br>' and line !='':
                        if line.split(',')[0] == 'Time':
                            columns = line.split(',')
                        else:
                            #print line
                            dt = to_datetime(str(date.month)+'/'+str(date.day)+ '/'+ str(date.year)+' '+line.split(',')[0])
                            print dt
                            line_data = line.split(',')[:-1]
                            ## append each line to dataframe
                            df = df.append(pd.DataFrame([line_data],index=[dt],columns=columns))
                        
            except:
                print 'skipped day'
                pass
        else:
            print 'passed'
            pass



    df = df.applymap(lambda x: np.nan if x=='-9999' else x)
    datafile =  df.to_csv('C:/Users/alex.messina/Documents/GitHub/SanDiegoBarometricPressure/Data/for Tommy/Barodata-'+site+'.csv')

baro = pd.DataFrame.from_csv('C:/Users/alex.messina/Documents/GitHub/SanDiegoBarometricPressure/Data/for Tommy/Barodata-'+site+'.csv')
baro['kPa'] = baro['PressureIn'] * 3.3863881579

baro['kPa'].plot()