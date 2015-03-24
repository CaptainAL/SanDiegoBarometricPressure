import urllib2
import os
import datetime
from BeautifulSoup import BeautifulSoup
from pandas import DataFrame, to_datetime, date_range
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

## Grabs weather data from NSTU Weather Station at Tafuna International Airport
## http://www.wunderground.com/history/airport/NSTU/2012/1/1/DailyHistory.html?theprefset=SHOWMETAR&theprefvalue=0
datagrab = True

now = datetime.datetime.now()

if datagrab == True:
    print 'Grabbing data...'
    s = 'KCRQ' ##stations needed
    daterange = date_range('20140101 00:00:00',now,freq='D')
    print '...from date range: '+str(daterange[0])+' to '+str(daterange[-1])
    columns = ['TimePST','TemperatureF','Dew PointF','Humidity','Sea Level PressureIn','VisibilityMPH','Wind Direction','Wind SpeedMPH','Gust SpeedMPH','PrecipitationIn','Events','Conditions','WindDirDegrees','DateUTC']
    datalist = [] ## write header columns in empty DataFrame
    for date in daterange:
        if date < now:
            print date
            try:
                url = 'http://www.wunderground.com/history/airport/'+s+'/'+str(date.year)+'/'+str(date.month)+'/'+str(date.day)+'/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=&format=1' ##enter web address of data
                print url
                page = urllib2.urlopen(url)
                soup = BeautifulSoup(page)
                soupsplit = str(soup.tagStack).split('\n')
                for line in soupsplit[2:-1]:
                    if line != None:
                        #print line
                        dt = to_datetime(str(date.month)+'/'+str(date.day)+ '/'+ str(date.year)+' '+line.split(',')[0])
                        data = line.split(',')
                        datalist.append((dt,data)) ##append tuple to list
                        print dt
            except:
                print 'skipped day'
                pass
        else:
            print 'passed'
            pass
    frame = DataFrame.from_items(datalist,orient='index',columns=columns)
    frame.columns = columns
    frame = frame.applymap(lambda x: np.nan if x=='-9999' else x)
    datafile =  frame.to_csv('C:/Users/Alex/Documents/GitHub/SanDiegoBarometricPressure/Data/Data-'+s+'.csv')
    
#### Append all
##files = os.listdir('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTP6/')
##alldata = open('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTP6/'+'2013.txt','w')
##for f in files:
##    if f.endswith('.csv')==True:
##        print f
##        with open(f,'wb') as csvfile:
##            data=csv.reader(csvfile,dialect='excel')
##            for row in data:
##                alldatata.write(row)
        
## Analyze data
##files = os.listdir('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTP6')
##barolist = []
##for f in files:
##    if f.endswith('.csv') == True:
##        print f
##        data = open(f,'r')
##        for line in data:
##            d = line.strip('\n').split()
##            if d[0].isdigit()==True:
##                year,month,day = d[0],d[1],d[2]
##                hour,minute = d[3],d[4]
##                time = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute))
##                pressure = d[12]
##                #print pressure
##                barolist.append((time,pressure))




