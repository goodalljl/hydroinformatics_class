#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides functions for plotting time series stored in ODM.

"""

import pymysql
import matplotlib.pyplot as plt
from matplotlib import dates

__author__ = "Jon Goodall"
__copyright__ = "Copyright 2014, Jon Goodall"
__credits__ = ["Jon Goodall"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jon Goodall"
__email__ = "goodall@virginia.edu"
__status__ = "alpha"

def get_timeseries(SiteID, VariableID):
    """Gets a time series from the LBRODM_small MySQL database
    
    Retrieves only the LocalDateTime and DataValue fields. Returns only raw 
    data (QualityControlLevel=1).
    
    Arguments:
        SiteID - the SiteID field for the time series
        VariableID - the VariableID field in ODM for the time series
    Returns:
        LocalDateTimes - the date/times for the time series in the local time zone
        DataValues - the values for the time series
    """
    
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', \
                db='LBRODM_small')
    sql_statement = "SELECT LocalDateTime, DataValue FROM DataValues \
                WHERE \
                SiteID = " + str(SiteID) + " AND \
                VariableID = " + str(VariableID) + " AND \
                QualityControlLevelID = 1 \
                ORDER BY LocalDateTime"
    cursor = conn.cursor()
    cursor.execute(sql_statement)
    rows =  cursor.fetchall()
    cursor.close()
    conn.close()
    LocalDateTimes, DataValues = zip(*rows)
    return LocalDateTimes, DataValues

def get_site_name(SiteID):
    """ Gets the SiteName field for a given SiteID value.
    
    Uses the LBRODM_small database. 
    
    Arguments:
        SiteID 
        
    Returns:
        SiteName
    """
    conn = pymysql.connect(host='localhost', port=3306, user='root', \
                passwd='', db='LBRODM_small')
    sql_statement = "SELECT SiteName FROM Sites \
                WHERE SiteID = " + str(SiteID)
    cursor = conn.cursor()
    cursor.execute(sql_statement)
    rows =  cursor.fetchall()
    cursor.close()
    conn.close()
    return rows[0][0] #Assumes one and only one row is returned with one and
                            #and only one field
    
def create_new_figure():
    """Creates a new figure for time series plots. 
    
    Sets properities for figure.
    
    Arguments:
        None
        
    Returns:
        fig - the figure object
    """
    
    fig = plt.figure()
    
    from matplotlib import rc
    font = {'family' : 'normal',
            'weight' : 'normal',
            'size'   : 12}
    rc('font', **font)
 
    return fig
    
def configure_subplot(ax, title):
    """Configures a new subplot for a figure.
    
    Sets default properties include the title of the subplot. 
    
    arguments:
        ax - the axes object
        title - the title for the subplot
    returns:
        N/A
    """
    ax.set_title(title)
    ax.set_ylabel("Temperature ($^\circ$C)") #hardcoded for now
    ax.set_xlabel("Date/Time") # hard coded for now
    ax.xaxis.set_minor_locator(dates.MonthLocator())
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.YearLocator())
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%Y'))
    ax.grid(True)
    
if __name__ == '__main__':    #code to execute if called from command-line

    fig = create_new_figure()
    
    ax = fig.add_subplot(211) #2 rows, 1 column, 1st plot
    configure_subplot(ax, get_site_name(1))
    
    dateTimes, dataValues = get_timeseries(2, 36)
    
    ax.plot(dateTimes, dataValues, color='black', linestyle='solid', markersize=0)
    
    ax2 = fig.add_subplot(212) #2 rows, 1 column, 2nd plot
    configure_subplot(ax2, get_site_name(2))
    
    dateTimes, dataValues = get_timeseries(4, 36)
    ax2.plot(dateTimes, dataValues, color='black', linestyle='solid', markersize=0)
    
    fig.tight_layout()
    fig.savefig("plot1.png")





