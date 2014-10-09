#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple demo of using PyMySQL and matplotlib to create a series data plot
from data stored in an ODM database.
"""

import pymysql
import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib import rc
import datetime

#inputs
SiteID = '2'
VariableID = '36'
StartLocalDateTime = "'2008-01-01'"
EndLocalDateTime = "'2008-12-31'"

#connect to database
conn = pymysql.connect(host='localhost', port=3306, user='root', \
        passwd='', db='LBRODM_small')

#extract time series from database
sql_statement = 'SELECT LocalDateTime, DataValue FROM DataValues \
        WHERE SiteID = ' + SiteID + ' AND VariableID = ' + VariableID + ' AND \
        QualityControlLevelID = 1 AND LocalDateTime >= ' + StartLocalDateTime \
        + ' AND LocalDateTime <= ' + EndLocalDateTime + \
        ' ORDER BY LocalDateTime'
cursor = conn.cursor()
cursor.execute(sql_statement)
rows =  cursor.fetchall()
localDateTimes, dataValues = zip(*rows)

#create plot
fig = plt.figure()
ax = fig.add_subplot(211)
ax.plot(localDateTimes, dataValues, color='grey', linestyle='solid', \
        markersize=0)

#set plot properties
ax.set_ylabel("Temperature ($^\circ$C)")
ax.set_xlabel("Date/Time")
ax.xaxis.set_minor_locator(dates.MonthLocator())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
ax.xaxis.set_major_locator(dates.YearLocator())
ax.xaxis.set_major_formatter(dates.DateFormatter('\n%Y'))
ax.grid(True)
ax.set_title('Water temperature at Little Bear River \n at McMurdy Hollow \
near Paradise, Utah') #hard coded for now. Should update when SiteID is updated.
fig.tight_layout()

#inputs
SiteID = '1'
VariableID = '36'
StartLocalDateTime = "'2008-01-01'"
EndLocalDateTime = "'2008-12-31'"

#connect to database
conn = pymysql.connect(host='localhost', port=3306, user='root', \
        passwd='', db='LBRODM_small')

#extract time series from database
sql_statement = 'SELECT LocalDateTime, DataValue FROM DataValues \
        WHERE SiteID = ' + SiteID + ' AND VariableID = ' + VariableID + ' AND \
        QualityControlLevelID = 1 AND LocalDateTime >= ' + StartLocalDateTime \
        + ' AND LocalDateTime <= ' + EndLocalDateTime + \
        ' ORDER BY LocalDateTime'
cursor = conn.cursor()
cursor.execute(sql_statement)
rows =  cursor.fetchall()
localDateTimes, dataValues = zip(*rows)

#create plot
#fig = plt.figure()
ax = fig.add_subplot(212)
ax.plot(localDateTimes, dataValues, color='grey', linestyle='solid', \
        markersize=0)

#set plot properties
ax.set_ylabel("Temperature ($^\circ$C)")
ax.set_xlabel("Date/Time")
ax.xaxis.set_minor_locator(dates.MonthLocator())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
ax.xaxis.set_major_locator(dates.YearLocator())
ax.xaxis.set_major_formatter(dates.DateFormatter('\n%Y'))
ax.grid(True)
ax.set_title('Water temperature at Little Bear River \n at Mendon Road near \
Mendon, Utah') #hard coded for now. Should update when SiteID is updated.
fig.tight_layout()

#set font type and size for plot
font = {'family' : 'sans-serif', #changed from 'normal' to remove warning
'weight' : 'normal',
'size' : 12}
rc('font', **font)

fig.savefig('plot1.png')
