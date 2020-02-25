#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:48:40 2019

@author: Mitchell
"""

import ee
ee.Initialize()
from assets import RawChirps, ModisRaw, Landsat8RealTimeRaw, Landsat7RealTimeRaw, fullCampsCollection, camps_ref_dict


#interval could = 'day', 'mmonth', 'year', etc
#index list is list of indices for desired camps --- i.e. [0,4,9]

def make_custom_FC(index_list, reference_dict):
#    make ee list of names of camps
    name_list = []
    for index in index_list:
        name_list.append(reference_dict[index])
    for i in range(len(name_list)):
        print("Getting statistics for: {}.".format(name_list[i]))
    name_list_ee = ee.List(name_list)

#    map over this list to create a custom feature collection

    def custom_name_map(name):
        select_camp = ee.Feature(fullCampsCollection.filterMetadata('name', 'equals', name).first())
        return select_camp


    custom_FC = ee.FeatureCollection(name_list_ee.map(custom_name_map))


    return custom_FC






def create_collection(start_str, end_str, interval, index_list):

    # ------------- variables to set -------------
    startDate = ee.Date(start_str)
    endDate = ee.Date(end_str) # june of 2018 for testing



    campsCollection = make_custom_FC(index_list, camps_ref_dict)
#   print(campsCollection.getInfo())

    if interval == 'day':
        ndviAdjust = -70
    elif interval =='month':
        ndviAdjust = -2
    else:
        ndviAdjust = 0




    #--------------- data sets -------------------------
    ChirpsDataSet = RawChirps.filterDate(startDate, endDate.advance(1,"day")).filterBounds(campsCollection).select("precipitation")

    ModisDataSet = ModisRaw.filterDate(startDate, endDate.advance(1,"day")).filterBounds(campsCollection).select("LST_Day_1km")

    def normalizeTemp(image):
        returnImage = (image.multiply(0.02).subtract(273.15)).copyProperties(**{'source': image,
                        'properties': ee.List(["system:index","system:time_end","system:time_start"])})
        return returnImage


    # ---------create compound landsat 7 and 8-------
    # algorithm: if start date during or later than 2014, use landsat 8 exclusively
    #            if start date before 2014 and if end date after, combine the two
    #                                          if end date before, use only landsat 7
#    for now just creating collection in assets.py


        
    backStart = startDate.advance(ndviAdjust, interval)
    LandsatDataSet = Landsat8RealTimeRaw.filterDate(backStart, endDate.advance(1,"day")).filterBounds(campsCollection)
    LST = ModisDataSet.map(normalizeTemp)
    Precip = ChirpsDataSet


    # -------------- mapping -----------------------------------

    dateDifference = endDate.difference(startDate, interval).round()

    #function to map over list of camps
    def campsMapping(feature):
        feature = ee.Feature(feature)


        adjustmentList = ee.List.sequence(0, dateDifference.toInt())

          #function to map over list of day adjustment numbers
        def dateListMapping(dateAdjust):
        #function to compute stats of each index
            def computeStats(indexFeature):
                indexFeature = ee.Feature(indexFeature)
                #reduction variables
                scale = 10
                maxPixels = 1e9

                Image = indexFeature.get('image')
                meanDict = ee.Image(Image).reduceRegion(**{
                    'reducer': ee.Reducer.mean(),
                    'geometry': feature.geometry(),
                    'scale': scale,
                    'maxPixels': maxPixels
                })
                meanStat = ee.Number(meanDict.values())
                return indexFeature.set(ee.Dictionary({'mean': meanStat,
                                                 'region': feature.get("name"),
                                                 'date': startDate.advance(dateAdjust, interval)}))

            newDate1 = startDate.advance(dateAdjust, interval)
            newDate2 = newDate1.advance(1, interval)

            #take mean of date in order to create single image
            PrecipImage = Precip.filterDate(newDate1,newDate2).filterBounds(feature.geometry()).mean()
            LSTImage = LST.filterDate(newDate1, newDate2).filterBounds(feature.geometry()).mean()
            
#           ----------- old ndvi calculations
            landsatFiltered = LandsatDataSet.filterDate(newDate1.advance(ndviAdjust, interval), newDate2).filterBounds(feature.geometry())
            composite = ee.Algorithms.Landsat.simpleComposite(**{
                                              'collection': landsatFiltered,
                                              'asFloat': True})
            NDVIImage = composite.normalizedDifference(ee.List(['B5','B4']))
#            -----------------
#            -----------new ndvi calculations
##            NDVIImage = ee.Algorithms.If(landsatFiltered.size(), landsatFiltered.mean(), (ee.Algorithms.Landsat.simpleComposite(**{
#                                          'collection': landsatFiltered,
#                                          'asFloat': True
#                                          })).normalizedDifference(['B5','B4']))
           
            
            

            #create features for all of the images
            precipFeature = ee.Feature(feature.geometry(), ee.Dictionary({'image': PrecipImage,'index': "Precipitation"}))
            LSTFeature = ee.Feature(feature.geometry(), ee.Dictionary({'image': LSTImage,'index': "LandSurfaceTemperature"}))
            NDVIFeature = ee.Feature(feature.geometry(), ee.Dictionary({'image': NDVIImage,'index': "NDVI"}))

            indexCollection = ee.FeatureCollection(ee.List([precipFeature, LSTFeature, NDVIFeature]))
            statCollection = indexCollection.map(computeStats)

            return statCollection


        dateList = adjustmentList.map(dateListMapping)



        #return for campsMapping
        return ee.FeatureCollection(dateList).flatten()












     #end of feature collection
    compositeCollection = campsCollection.map(campsMapping).flatten()
    
    collection_info = compositeCollection.getInfo()
    
    print(collection_info)
#    print(type(collection_info))

    return compositeCollection, collection_info


def export(collection, filename):
    task = ee.batch.Export.table.toDrive(**{
      'collection': collection,
      'description':'fullStats1Python',
      'folder' : 'RemoteSensing',
      'fileNamePrefix' : filename,
      'fileFormat': 'CSV'
    })

    task.start()
