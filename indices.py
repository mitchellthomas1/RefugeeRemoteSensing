#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 21:31:12 2020

@author: Mitchell
"""

#Climate Change Indices - Calculations of some of the 27 core indices
#input file with just one camp, daily data over several years

#problem - on daily data there are many missing days in lst data
#solution - modeling distribution of months with more missing data and predict missing values


import pandas
import numpy as np
import matplotlib.pyplot as plt





#-----------the following functions take in a daily array which starts
#           on Jan 1 of year x and ends on Dec 31 of year z------------

#    take start year and end year in integer
#    and bool True or False if each stat is desired

def yearly_stats(array, start_yr, end_yr, R10mm = True, R20mm = True, PRCPTOT = True):
        
#20. R10mm Annual count of days when PRCP≥ 10mm:   
#21. R20mm Annual count of days when PRCP≥ 20mm
#23. CDD. Maximum length of dry spell, maximum number of consecutive days with RR < 1mm:
#    create array with m rows for each year and n columns for 1 year and each statistic
#    make sizes and array
    n_columns = 1 + int(R10mm) + int(R20mm) + int(PRCPTOT)
    m_rows = end_yr - start_yr + 1
    yearly_arr = np.empty((m_rows, n_columns))

    year_R10 = 0
    year_R20 = 0
    year_prcptot = 0
#    loop through each line, and add to yearly variables each time
#    when year changes: add those stats to table, and change to new year
    
    for line in array:
        precip = line[2]
        lst = line[3]
        year = int(line[1][0:4])
        if year not in yearly_arr:
#            fill in previous year with total variables
            prev_year = year - 1
            prev_row = prev_year - start_yr
            yearly_arr[prev_row][1] = year_R10
            yearly_arr[prev_row][2] = year_R20
            yearly_arr[prev_row][3] = year_prcptot
            
#            add new year to new row
            new_row = year - start_yr
#            print(new_row)
            yearly_arr[new_row][0] = year
            
#            print(yearly_arr)
#            reset variables
            year_R10 = 0
            year_R20 = 0
            year_prcptot = 0
            
#        check for R10:
        if precip >= 10.0:
            year_R10 += 1
        if precip >= 20.0:
            year_R20 += 1
#            wet day defined as a millimter or more of rainfall
        if precip > 1.0:
            year_prcptot += precip
            
    yearly_arr[-1][1] = year_R10
    yearly_arr[-1][2] = year_R20
    yearly_arr[-1][3] = year_prcptot
            
    return yearly_arr


#filename in csv, yearly stats should input daily csv starting
#    on 
def run_stats(filename, yearly_stats = True, interval_stats = False, 
          interval_start = None, interval_end = None):
    return 0
    
    

filename = "CoxBazar2014to2019daily.csv"

raw_table = pandas.read_csv(filename)
array = raw_table.values
#print(array)
head_text = "    year           R10mm          R20mm              PRCPTOT"
print(head_text)  

final_table = yearly_stats(array, 2014, 2019)
print(final_table)
            
            
        
        

#-------------Stuart - Ignore after this------------



























##number of days of data for each stat
#n_precip = 0
#n_ndvi = 0
#n_lst = 0
#
##total number of days for each stat
#total_days = 0
#
#for line in array:
#    if math.isnan(line[2]) == False:
#        n_precip += 1
#    if math.isnan(line[3]) == False:
#        n_lst += 1
#    total_days += 1
#        
#print("% precip: ", n_precip/total_days)
#print("% lst: ", n_lst/total_days)
#
#print(type(array[0][3]))
#
##generate stats on bad data
##dictionary with keys of each year
##which point to dictionaries for each year
##these yearly dictionaries point each month 
##to a size 2 list which gives the number of days 
##in each month that [precip, lst] is null
#
#stat_dict = {}
#for line in array:
#    year = str(line[1])[:4]
#    month = str(line[1])[5:7]
#    day = str(line[1])[8:10]
#    
#    if year not in stat_dict:
#        stat_dict[year] = {}
#    
#    if month not in stat_dict[year]:
#        stat_dict[year][month] = 0
#        
#    if math.isnan(line[3]):
#        stat_dict[year][month] += 1
#        
##print(stat_dict)
#    
#keys = stat_dict['2018'].keys()
#values = stat_dict['2018'].values()
#
#print(keys)
#print(values)
#
#plt.plot(keys, values)
#plt.xlabel("month of 2018")
#plt.ylabel("number of null data points")
#plt.savefig("2018lstnulldays")


    
    



#SU - Number of Summer Days
#Annual count of days when TX (dailymaximum temperature) > 25oC.
def su(file, n_camps):
    return 0




































    