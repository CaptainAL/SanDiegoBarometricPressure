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
    daterange = date_range('20161017 00:00:00',now,freq='D')
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
    
baro = pd.DataFrame.from_csv('C:/Users/Alex/Documents/GitHub/SanDiegoBarometricPressure/Data/Data-'+s+'.csv')
baro['kPa'] = baro['Sea Level PressureIn'] * 3.3863881579

   
XL= pd.ExcelFile('C:/Users/Alex/Documents/GitHub/SanDiegoBarometricPressure/Data/PT_and_baro_data.xlsx')
EDC20 = XL.parse('EDC20',header=13,parse_cols='A,B,D',parse_dates=[['Date','Time']],index_col=['Date_Time'])
EDC20 = EDC20.resample('15Min',how='mean')
EDC20['baropressure'] = baro['kPa'].resample('15Min',how='mean')
EDC20['stage_cm'] = (EDC20['LEVEL']-EDC20['baropressure']) *.102*100.0
EDC20['stage_ft'] = EDC20['stage_cm']/2.54/12
EDC20_daily = EDC20['stage_ft'].resample('1D',how='mean')
EDC20_daily.to_csv('C:/Users/Alex/Documents/GitHub/SanDiegoBarometricPressure/Data/EDC20 daily mean ft.csv')

EDC50 = XL.parse('EDC50',header=13,parse_cols='A,B,D',parse_dates=[['Date','Time']],index_col=['Date_Time'])
EDC50 = EDC50.resample('15Min',how='mean')
EDC50['baropressure'] = baro['kPa'].resample('15Min',how='mean')
EDC50['stage_cm'] = (EDC50['LEVEL']-EDC50['baropressure']) *.102*100.0
EDC50['stage_ft'] = EDC50['stage_cm']/2.54/12
EDC50_daily = EDC50['stage_ft'].resample('1D',how='mean')
EDC50_daily.to_csv('C:/Users/Alex/Documents/GitHub/SanDiegoBarometricPressure/Data/EDC50 daily mean ft.csv')

field_measurements_EDC20 = XL.parse('Field_measurements',parse_dates=['Date'],index_col=['Date'])
field_measurements_EDC20['EDC20_daily_stage_ft'] = EDC20_daily
field_measurements_EDC20['Field-PT-difference'] = field_measurements_EDC20['Depth (ft)'] -field_measurements_EDC20['EDC20_daily_stage_ft']
field_measurements_EDC20.to_csv('C:/Users/Alex/Documents/GitHub/SanDiegoBarometricPressure/Data/EDC20 field vs PT.csv')

field_measurements_EDC50 = XL.parse('Field_measurements',parse_dates=['Date'],index_col=['Date'])
field_measurements_EDC50['EDC50_daily_stage_ft'] = EDC50_daily
field_measurements_EDC50['Field-PT-difference'] = field_measurements_EDC50['Depth (ft)'] -field_measurements_EDC50['EDC50_daily_stage_ft']
field_measurements_EDC50.to_csv('C:/Users/Alex/Documents/GitHub/SanDiegoBarometricPressure/Data/EDC50 field vs PT.csv')


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




