#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple demo of using Pandas to visualize time series data
"""

import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#edit for your specific ODM database
conn = pymysql.connect(host='localhost', port=3306, user='root', \
        passwd='', db='LBRODM_small')
cursor = conn.cursor()

#hard coded to plot water temperature observations at SiteID = 2
sql_statement = "SELECT LocalDateTime, DataValue FROM DataValues \
        WHERE SiteID = 2 AND VariableID = 36 ORDER BY LocalDateTime"
cursor.execute(sql_statement)
rows =  cursor.fetchall()

localDateTimes, dataValues = zip(*rows)

ts = pd.Series(dataValues, index=localDateTimes)

fig, axes = plt.subplots(nrows=2, ncols=2)

ts.plot(ax=axes[0,0])
axes[0,0].set_title('Temperature at SiteID=2')

ts.resample('W', how=['mean', np.min, np.max]).plot(ax=axes[0,1]) 
axes[0,1].set_title('Weekly Resample')

ts.resample('M', how=['mean', np.min, np.max]).plot(ax=axes[1,0]) 
axes[1,0].set_title('Monthly Resample')

df = pd.DataFrame(ts, columns=['tmp'])
df['mon'] = df.index.month
df.boxplot(column = 'tmp', by='mon', ax=axes[1,1]) 
axes[1,1].set_title('Monthly Boxplot')
fig = axes[1][1].get_figure()
fig.suptitle('')

plt.tight_layout()
plt.savefig('Class_14_InClassDemoPandas.png')
plt.show()