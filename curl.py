#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 18:04:26 2020

@author: Mitchell
"""

import requests
res = requests.get('''https://chc-ewx2.chc.ucsb.edu:8919/rest/timeseries/version/3.0/vector_dataset/africa:g2008_af_1/raster_dataset/chirps/region/africa/periodicity/1-month/statistic/data/lat/7.766884688797074/lon/34.25840059276797/seasons/1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,stm/calculation_type/mean/mean-median/true''')
print(res.json())
#temp = res.json()
#print(temp)