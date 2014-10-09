#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides TimeSeries class for plotting time series stored in ODM.

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

class TimeSeries():
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they should be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section.

    Attributes:
    attr1 (str): Description of `attr1`.
    attr2 (list of str): Description of `attr2`.
    attr3 (int): Description of `attr3`.

    """
    
    def __init__(self, SiteID, VariableID):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
          Do not include the `self` parameter in the ``Args`` section.

        Args:
          param1 (str): Description of `param1`.
          param2 (list of str): Description of `param2`. Multiple
            lines are supported.
          param3 (int, optional): Description of `param3`, defaults to 0.

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
        self.LocalDateTimes = LocalDateTimes
        self.DataValues = DataValues
    
        conn = pymysql.connect(host='localhost', port=3306, user='root', \
                    passwd='', db='LBRODM_small')
        sql_statement = "SELECT SiteName FROM Sites \
                    WHERE SiteID = " + str(SiteID)
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        rows =  cursor.fetchall()
        cursor.close()
        conn.close()
        self.SiteName = rows[0][0]
    
    def plot(self):
        """Class methods are similar to regular functions.

        Note:
          Do not include the `self` parameter in the ``Args`` section.

        Args:
          param1: The first parameter.
          param2: The second parameter.

        Returns:
          True if successful, False otherwise.

        """
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        from matplotlib import rc
        font = {'family' : 'normal',
                'weight' : 'normal',
                'size'   : 12}
        rc('font', **font)
        ax.set_ylabel("Temperature ($^\circ$C)") #hard coded for now
        ax.set_xlabel("Date/Time") #hard coded for now
        ax.xaxis.set_minor_locator(dates.MonthLocator())
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
        ax.xaxis.set_major_locator(dates.YearLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('\n%Y'))
        
        ax.grid(True)
        ax.plot(self.LocalDateTimes, self.DataValues)
        ax.set_title(self.SiteName)

        fig.tight_layout()
        fig.show()

if __name__ == '__main__':    #code to execute if called from command-line

    ts = TimeSeries(2, 36)
    ts.plot()


