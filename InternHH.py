# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 22:22:54 2021

@author: MRITYUNJAY
Working on the data
"""

import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
ISEGlobal = pd.read_csv('ISELGlobal_REVIEWS_GENERAL.csv')
ISEGlobal
ISEGlobal.dropna(how = 'all', inplace = True)

dt = ISEGlobal[ISEGlobal['Platform']=='Facebook'].Date
dt.replace('Junuary 4, 2018', 'January 4, 2018', inplace = True)
new_dt = pd.Series([datetime.strptime(i, '%B %d, %Y') for i in dt])
dt[dt == 'Junuary 4, 2018']
dt
fb_new_date = pd.Series([i.date() for i in new_dt])
ISEGlobal.replace(ISEGlobal[ISEGlobal['Platform'] == 'Facebook'].Date,new_dt, inplace = True)

dt = ISEGlobal[ISEGlobal['Platform']=='Twitter'].Date
dt
twit_new_date = pd.Series([datetime.strptime(i, '%a %b %d %H:%M:%S %z %Y').date() for i in dt])
twit_new_date

f_date = fb_new_date
f_date = f_date.append(twit_new_date, ignore_index=True)

dt = ISEGlobal[ISEGlobal['Platform']=='ISEL Global'].Date
dt
dt = [i.strip("On ") for i in dt]
dt = [i.strip("\xa0") for i in dt]
dt
ISE_new_dt = pd.Series([datetime.strptime(i, '%B %d, %Y').date() for i in dt])
ISE_new_dt

f_date = f_date.append(ISE_new_dt, ignore_index = True)
f_date

dt = ISEGlobal[ISEGlobal['Platform']=='Google Reviews'].Date
dt = [i.strip(" ago") for i in dt]
dt
dt = pd.Series(dt)
dt[160 : 200]
dt[dt == '28 minutes'] = '1 day'
dt[dt == 'day'] = '1 day'
dt[dt == 'month'] = '1 month'
dt[dt == 'year'] = '1 year'
dt[dt == 'week'] = '1 week'

def get_past_date(str_days_ago):
    TODAY = datetime.now()
    splitted = str_days_ago.split()
    if splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
        date = datetime.datetime.now() - relativedelta(hours=int(splitted[0])+24)
    elif splitted[1].lower() in ['day', 'days', 'd']:
        date = TODAY - relativedelta(days=int(splitted[0])+1)
    elif splitted[1].lower() in ['wk', 'wks', 'week', 'weeks', 'w']:
        date = TODAY - relativedelta(weeks=int(splitted[0]))
    elif splitted[1].lower() in ['mon', 'mons', 'month', 'months', 'm']:
        date = TODAY - relativedelta(months=int(splitted[0]))
    elif splitted[1].lower() in ['yrs', 'yr', 'years', 'year', 'y']:
        date = TODAY - relativedelta(years=int(splitted[0]))
    else:
        return "Wrong Argument format"
    return date

google_new_dates = pd.Series([get_past_date(i).date() for i in dt])
google_new_dates

f_date = f_date.append(google_new_dates, ignore_index = True)
f_date
ISEGlobal.shape
ISEGlobal['Formatted Dates'] = f_date
ISEGlobal.columns
finalISEGlobal = ISEGlobal.drop('Date', axis=1)
finalISEGlobal.to_csv('finalData.csv')

#Yeah we have our data, now can finally work on it... Sentiment and all ... :)
finalISEGlobal
ise = pd.read_csv('iselglobal_website.csv')
ise.columns
courses = ise['rv-course 2'].unique()
courses = courses[~pd.isnull(courses)]
courses = list(courses)
courses = [i.lower() for i in courses]
courses


