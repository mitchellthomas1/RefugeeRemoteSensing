#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:49:20 2019

@author: Mitchell
"""
import ee
ee.Initialize

RawChirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
ModisRaw = ee.ImageCollection("MODIS/006/MOD11A1")
Landsat8RealTimeRaw = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT")
Landsat7RealTimeRaw = ee.ImageCollection("LANDSAT/LE07/C01/T1_RT")

fullCampsCollection = ee.FeatureCollection("users/mlt2177/CampsShapeFiles")



Landsat72013 = Landsat7RealTimeRaw.filterDate('1999-01-01','2013-04-13')


camps_ref_dict = {0: 'Kakuma',
                1 : 'Hagadera',
                2 : 'Dagahaley',
                3 : 'Ifo', 
                4 : 'Al Hawl',
                5 : 'Palorinya',
                6 : 'Nyumazni',
                7 : 'Nguenyyiel', 
                8 : 'Pugnido', 
                9 : 'Melkadida', 
                10 : 'Nduta',
                11 : 'Mtendeli', 
                12 : 'Nyarugusu',
                13 : 'Cox Bazar', 
                14 : 'Bidibidi', 
                15 : 'Yida', 
                16 : 'Pamir', 
                17 : 'Ajuongthok'}

camps_ref_dict_full = {0: 'Kakuma, Kenya',
                1 : 'Hagadera, Kenya',
                2 : 'Dagahaley, Kenya',
                3 : 'Ifo, Kenya', 
                4 : 'Al Hawl, Syria',
                5 : 'Palorinya, Uganda',
                6 : 'Nyumazni, Uganda',
                7 : 'Nguenyyiel, Ethiopia', 
                8 : 'Pugnido, Ethiopia', 
                9 : 'Melkadida, Ethiopia', 
                10 : 'Nduta, Tanzania',
                11 : 'Mtendeli, Tanzania', 
                12 : 'Nyarugusu, Tanzania',
                13 : 'Cox Bazar, Bangladesh', 
                14 : 'Bidibidi, South Sudan', 
                15 : 'Yida, South Sudan', 
                16 : 'Pamir, South Sudan', 
                17 : 'Ajuongthok, South Sudan'}
                
                
                

#
#def iterate(feature, prev):
#    
#    prevString = ee.String(prev)
#    name = ee.String(feature.get("name"))
#    state = ee.String(feature.get("state"))
#    nameState = name.cat(",").cat(state).cat(";")
#    
#    return ee.String(prevString.cat(nameState))
#
#namesString = ee.String(fullCampsCollection.iterate(iterate, ""));
#
#print(namesString)


#def iterate(feature, prev):
#    
#    prevString = str(prev)
#    name = str(feature.get("name"))
#    state = str(feature.get("state"))
#    nameState = name + "," + state + ";" 
#    
#    return str(prevString + nameState)
#
#namesString = str(fullCampsCollection.iterate(iterate, ""));
#
#print(namesString)


#Bangladesh = ee.Geometry.Polygon([[92.13819732884394, 21.214905292606346],
#      [92.13751068333613, 21.21330500560197],
#      [92.13493576268183, 21.21266488594252],
#      [92.13493576268183, 21.21026441249875],
#      [92.13424911717402, 21.208664075185933],
#      [92.1357940695666, 21.20690368410764],
#      [92.1357940695666, 21.20402299889283],
#      [92.13493576268183, 21.200502085101277],
#      [92.13184585789668, 21.20018199786749],
#      [92.13184585789668, 21.196340896963463],
#      [92.13236084202754, 21.193139903257837],
#      [92.13459243992793, 21.190258949635506],
#      [92.13493576268183, 21.188498339219052],
#      [92.13476410130488, 21.185937413903158],
#      [92.13699569920527, 21.18385662941561],
#      [92.1354507468127, 21.183216382142792],
#      [92.1354507468127, 21.18033523510502],
#      [92.13630905369746, 21.17825437177483],
#      [92.13854065159785, 21.177774168386577],
#      [92.14214554051387, 21.177774168386577],
#      [92.14369049290644, 21.18097549485406],
#      [92.14695205906855, 21.18097549485406],
#      [92.15055694798457, 21.179855038473928],
#      [92.15347519139277, 21.178574506500716],
#      [92.15708008030879, 21.179374840283437],
#      [92.15862503270137, 21.18241606915278],
#      [92.15879669407832, 21.18545723546708],
#      [92.1606849692248, 21.18769805482401],
#      [92.16205826024043, 21.190258949635506],
#      [92.16205826024043, 21.19329995459005],
#      [92.16257324437129, 21.195380606133146],
#      [92.16549148777949, 21.196020800713512],
#      [92.16634979466426, 21.197461228376945],
#      [92.16634979466426, 21.199861909940093],
#      [92.16566314915644, 21.202422593937914],
#      [92.16549148777949, 21.204663156018935],
#      [92.16600647191035, 21.20642357380753],
#      [92.16652145604121, 21.20818397060964],
#      [92.16755142430293, 21.209624279655173],
#      [92.16772308567988, 21.211864732464818],
#      [92.16463318089473, 21.211704701248845],
#      [92.16205826024043, 21.211704701248845],
#      [92.15965500096308, 21.211544669859407],
#      [92.15828170994746, 21.21330500560197],
#      [92.15673675755488, 21.214105151272804],
#      [92.15450515965449, 21.214905292606346],
#      [92.15296020726191, 21.21602548318633],
#      [92.15124359349238, 21.213785093524944],
#      [92.14832535008418, 21.21330500560197],
#      [92.14626541356074, 21.215705429602423],
#      [92.14334717015254, 21.213785093524944],
#      [92.14025726536738, 21.21522534792528]])
#AlHawl = ee.Geometry.Polygon(
#    [[41.14867916957144, 36.38035620408946],
#      [41.135976227676906, 36.37890504755894],
#      [41.1341737832189, 36.384364019552045],
#      [41.125247391617336, 36.38298203755277],
#      [41.128766449844875, 36.37220173506031],
#      [41.127049836075344, 36.366188994300366],
#      [41.13134137049917, 36.36584342036641],
#      [41.13494625941519, 36.36107434334994],
#      [41.143529328262844, 36.361281700602035],
#      [41.14267102137808, 36.36432287682401],
#      [41.138036164200344, 36.364668457510895],
#      [41.13443127528433, 36.36805506702283],
#      [41.13631955043081, 36.37164885875855],
#      [41.14558926478628, 36.372961933559445],
#      [41.15159741297964, 36.369229978739355],
#      [41.154515656387844, 36.371234198953665],
#      [41.150739106094875, 36.375242484483636]])
#
#
#campsList = ee.List([ee.Feature(Bangladesh, {'name': 'Cox Bazar', 'state': 'Bangladesh'}),
#                            ee.Feature(AlHawl, {'name': 'Al Hawl', 'state': 'Syria'})])
#campsCollection = ee.FeatureCollection(campsList)
#
#
#
#OwenShapeCollection = ee.FeatureCollection("users/mlt2177/campmatrixSHP")
#classList = ee.List.sequence(1, 16)
#
#def combineClass(i):
#    classCollection = OwenShapeCollection.filterMetadata('class','equals',ee.Number(i))
#    classFeature = classCollection.union().first().set('class', ee.Number(i).toInt())
#    return ee.Feature(classFeature)
#
#
#combinedClassCollection = ee.FeatureCollection(classList.map(combineClass))
#
#print(combinedClassCollection.first().getNumber('class').getInfo())
#
#
## dict mapping class to name of camp
#OwenReferenceDict = ee.Dictionary({'1': ee.Dictionary({'name': 'Kakuma', 'state': 'Kenya'}),
#                '2': ee.Dictionary({'name': 'Hagadera', 'state': 'Kenya'}),
#                '3'  : ee.Dictionary({'name': 'Dagahaley', 'state': 'Kenya'}),
#                '4' : ee.Dictionary({'name': 'Ifo', 'state': 'Kenya'}),
#                '5' : ee.Dictionary({'name': 'Nguenyyiel', 'state': 'Ethiopia'}),
#                '6' : ee.Dictionary({'name': 'Bidibidi', 'state': 'South Sudan'}),
#                '7' : ee.Dictionary({'name': 'Yida', 'state': 'South Sudan'}),
#                '8' : ee.Dictionary({'name': 'Nduta', 'state': 'Tanzania'}),
#                '9' : ee.Dictionary({'name': 'Mtendeli', 'state': 'Tanzania'}),
#                '10' : ee.Dictionary({'name': 'Pugnido', 'state': 'Ethiopia'}),
#                '11' : ee.Dictionary({'name': 'Melkadida', 'state': 'Ethiopia'}),
#                '12' : ee.Dictionary({'name': 'Pamir', 'state': 'South Sudan'}),
#                '13' : ee.Dictionary({'name': 'Ajuongthok', 'state': 'South Sudan'}),
#                '14': ee.Dictionary({'name': 'Nyarugusu', 'state': 'Tanzania'}),
#                '15' : ee.Dictionary({'name': 'Palorinya', 'state': 'Uganda'}),
#                '16' : ee.Dictionary({'name': 'Nyumanzi', 'state': 'Uganda'}) })
#            

#
#    
#def shapeMap(feature):
#    feature = ee.Feature(feature)
#    classProp = ee.Number(feature.get('class')).getInfo()
#    propertyDict = OwenReferenceDict.get(classProp)
#    updatedFeature = feature.set(propertyDict)
#    return updatedFeature
#
#mappedShapes = combinedClassCollection.map(shapeMap);
#
#fullCampsCollection = campsCollection.merge(mappedShapes)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#OwenReferenceDict = ee.Dictionary({1: ee.Dictionary({'name': 'Kakuma', 'state': 'Kenya'}),
#                2: ee.Dictionary({'name': 'Hagadera', 'state': 'Kenya'}),
#                3  : ee.Dictionary({'name': 'Dagahaley', 'state': 'Kenya'}),
#                4 : ee.Dictionary({'name': 'Ifo', 'state': 'Kenya'}),
#                5 : ee.Dictionary({'name': 'Nguenyyiel', 'state': 'Ethiopia'}),
#                6 : ee.Dictionary({'name': 'Bidibidi', 'state': 'South Sudan'}),
#                7 : ee.Dictionary({'name': 'Yida', 'state': 'South Sudan'}),
#                8 : ee.Dictionary({'name': 'Nduta', 'state': 'Tanzania'}),
#                9 : ee.Dictionary({'name': 'Mtendeli', 'state': 'Tanzania'}),
#                10 : ee.Dictionary({'name': 'Pugnido', 'state': 'Ethiopia'}),
#                11 : ee.Dictionary({'name': 'Melkadida', 'state': 'Ethiopia'}),
#                12 : ee.Dictionary({'name': 'Pamir', 'state': 'South Sudan'}),
#                13 : ee.Dictionary({'name': 'Ajuongthok', 'state': 'South Sudan'}),
#                14: ee.Dictionary({'name': 'Nyarugusu', 'state': 'Tanzania'}),
#                15 : ee.Dictionary({'name': 'Palorinya', 'state': 'Uganda'}),
#                16 : ee.Dictionary({'name': 'Nyumanzi', 'state': 'Uganda'}) })
#







