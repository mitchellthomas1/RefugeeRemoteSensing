#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:03:15 2019

@author: Mitchell
"""
import ee
ee.Initialize

from accessGEE import create_collection, export
from assets import fullCampsCollection, camps_ref_dict, camps_ref_dict_full
import pandas
import time
import os.path
import datetime
import csv




def real_time():
    print("\nReal Time Monitoring: ")
    camp_input = int(input("select desired camp (1-18): "))
    rt_index_li = [camp_input - 1]

    input_date = input("Input date in form YYYY-MM-DD: ")
    output_tuple = input_date, input_date, "day", rt_index_li, False, "realtime"

    return output_tuple


def aggregate():
    
    index_list_agg = []
    print("\n Remote Sensing Refugee Camp Monitor")

    while True:
        user_input = input('''To add a camp to the final output, type its index (1-18) and press Enter.
                           Add camps as desired. When finished, type "done".
                           Enter here: ''')
        if user_input == 'done':
            break
        index_list_agg.append(int(user_input) - 1)
        
    interval = input('Would you like monthly, daily, or yearly averages? (type "month", "day", or "year"): ')

    start_date = input("Input start date in form YYYY-MM-DD: ")

    end_date = input("Input end date in form YYYY-MM-DD: ")



    return start_date, end_date, interval, index_list_agg, "aggregate"

def data_input():

#    camp_names = """Cox Bazar,Bangladesh;Al Hawl,Syria;
#    Kakuma,Kenya;Hagadera,Kenya;Dagahaley,Kenya;
#    Ifo,Kenya;Nguenyyiel,Ethiopia;Bidibidi,South Sudan;
#    Yida,South Sudan;Nduta,Tanzania;Mtendeli,Tanzania;
#    Pugnido,Ethiopia;Melkadida,Ethiopia;Pamir,South Sudan;
#    Ajuongthok,South Sudan;Nyarugusu,Tanzania;
#    Palorinya,Uganda;Nyumanzi,Uganda;""".strip()

#    camps_list = camp_names.split(';')[:-1]
    
    print('''Remote Sensing Monitoring of Global Refugee Camps:
        
Precipitation, NDVI, and Land Surface Temperature data currently
availabe for 18 global refugee camps''')

    print("\nAvailable Refugee Camps: ")

    for i in (camps_ref_dict_full):
        print(('[{}] --- {}').format(i+1,camps_ref_dict_full[i]))
        
    index_list = []

    while True:
        user_input = input('''To add a camp to the final output, type its index (1-18) and press Enter.
                           Add camps as desired. When finished, type "done".
                           Enter here: ''')
        if user_input == 'done':
            break
        index_list.append(int(user_input) - 1)
        
    interval = input('\nWould you like monthly, daily, or yearly averages? (type "month", "day", or "year"): ')
    start_date = input("\nInput start date in form YYYY-MM-DD: ")
    end_date = input("Input end date in form YYYY-MM-DD: ")

    return start_date, end_date, interval, index_list






def parse_data(csv_file, camp_input, date_input):
    raw_table = pandas.read_csv(csv_file)
    raw_table_values = raw_table.values

    print(raw_table_values)

    index_dict = {}
    for line in raw_table_values:
        date = str(line[1])[0:10]
    #    print(date)
        camp = str(line[5])
        index_dict[line[3]] = line[4][1:-1]

    print(index_dict)
    index_str = '''
    For camp in {} on {},

            Precipitation (mm) = {}
            Average Land Surface Temperature (C) =  {}
            Average NDVI across past 60 days = {}
                    '''.format(camp_input, date_input,
                    index_dict['Precipitation'],
                    index_dict['LandSurfaceTemperature'],
                    index_dict['NDVI'])

    print(index_str)
    
def parse_json(collection_info, index_list, file_prefix):
    feature_li = collection_info['features']
#    width of array is number of indices
#    lenth is 
#    plan:
#    make header, write header: date , index1, index2, etc..
#    each line is the date, and then the mean value for each thing
    save_path = 'C:ToolV5/csvfiles/'
    filename = os.path.join(save_path, file_prefix + ".csv") 
    with open(filename, mode='w') as csv_file:
        
        header = ['date'] + index_list
        
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
#        writer.writerow({'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'})
#        writer.writerow({'emp_name': 'Erica Meyers', 'dept': 'IT', 'birth_month': 'March'})
    
        write_dict = {'date': None}
        for element in feature_li:
#            print(element['properties'].keys())
            datems = element['properties']['date']['value']
#            put into python datetime format, advance one day to account for bug in transferring
            date_object = (datetime.datetime.fromtimestamp(datems/1000.0) 
                                + datetime.timedelta(days = 1))
            date_str = date_object.strftime('%x')
            if date_str != write_dict['date']:
                writer.writerow(write_dict)
                write_dict = {'date' : date_str}
                
            index = element['properties']['index']
            mean = element['properties']['mean'][0]
            if mean == None:
                mean = "null"
            write_dict[index] = mean
            
            
    
       
        

            
#        array_width = len(feature_li)/num_indices
    
    
    





if __name__ == '__main__':


    start_date, end_date, interval, index_list = data_input()
    
    camp_string = ""
    for index in index_list:
        camp_string += camps_ref_dict[index]
    file_prefix = camp_string.replace(" ", "") + interval + str(round(time.time()))

    



    collection, collection_info = create_collection(start_date, end_date, interval, index_list)
    stat_indices =['Precipitation','LandSurfaceTemperature','NDVI']
    parse_json(collection_info, stat_indices, 'JSON'+ file_prefix)
     
    

