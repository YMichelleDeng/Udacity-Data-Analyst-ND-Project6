#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script is used to parse the flight 2008.csv file into small datafiles for visualization.
"""

""" Load the csv file """
import pandas as pd
import pprint

# Read the file
data = pd.read_csv("2008.csv", low_memory = True)

# Output the number of rows
print ("Total rows: {0}".format(len(data)))

# See which headers are available
# print (list(data))

""" Group by Carrier Origin """

Origin = data[['UniqueCarrier','DepDelay','Origin']]
df1 = pd.DataFrame(Origin)

df1['Dep_route_count'] = 1  # create a new column named 'route_count'

df1['DepDelay_count'] = '0'  # create a new column named 'DepDelay_count'
df1.loc[df1['DepDelay'] > 0, 'DepDelay_count'] = 1  
df1.loc[(df1['DepDelay'] < 0) & (df1['DepDelay'] == 0), 'DepDelay_count'] = 0

df1['Dep_route_count'] = df1['Dep_route_count'].astype('float64')   # change dtype from object ot float64
df1['DepDelay_count'] = df1['DepDelay_count'].astype('float64')

print ("Total Origin_airports: {0}".format(len(df1.groupby([df1.Origin]).size())))
print ((df1.groupby([df1.Origin]).size()).order(ascending = False)[:20])

top20airpots_orig = ['ATL','ORD','DFW','DEN','LAX','PHX','IAH','LAS','DTW','SFO','SLC','EWR','MCO',
                'MSP','CLT','LGA','JFK','BOS','SEA','BWI']

df2 = pd.DataFrame(df1[df1['Origin'].isin(top20airpots_orig)])

carrier_origin = df2.groupby(['Origin','UniqueCarrier']).sum()
carrier_origin['DepDelay_ratio'] = carrier_origin['DepDelay_count']/carrier_origin['Dep_route_count']*100



""" Group by Carrier Dest """

Dest = data[['UniqueCarrier','ArrDelay','Dest']]
df3 = pd.DataFrame(Dest)

df3['Arr_route_count'] = 1

df3['ArrDelay_count'] = '0'
df3.loc[df3['ArrDelay'] > 0, 'ArrDelay_count'] = 1  
df3.loc[(df3['ArrDelay'] < 0) & (df3['ArrDelay'] == 0), 'ArrDelay_count'] = 0

df3['Arr_route_count'] = df3['Arr_route_count'].astype('float64')    
df3['ArrDelay_count'] = df3['ArrDelay_count'].astype('float64')

print ("Total Dest_airports: {0}".format(len(df3.groupby([df3.Dest]).size())))
print ((df3.groupby([df3.Dest]).size()).order(ascending = False)[:20])

top20airpots_dest = ['ATL','ORD','DFW','DEN','LAX','PHX','IAH','LAS','DTW','SFO','SLC','EWR','MCO',
                'MSP','CLT','LGA','JFK','BOS','SEA','BWI']

df4 = pd.DataFrame(df3[df3['Dest'].isin(top20airpots_dest)])

carrier_dest= df4.groupby(['Dest','UniqueCarrier']).sum()
carrier_dest['ArrDelay_ratio'] = carrier_dest['ArrDelay_count']/carrier_dest['Arr_route_count']*100



""" Write out csv files """
carrier_origin.to_csv('flight2008_carrier_origin.csv')
carrier_dest.to_csv('flight2008_carrier_dest.csv')


