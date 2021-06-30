import fetch_option_chain
import pandas as pd
import numpy as np

'''
Returns a boolean whether the data can be a support or not
'''

def isSupport(df,i):
    support1 = df['Put_OI'][i] > df['Put_OI'][i-1]  and df['Put_OI'][i] > df['Put_OI'][i+1] and df['Put_OI'][i] > df['Put_OI'][i+2] and df['Put_OI'][i] > df['Put_OI'][i-2]
    support2 = df['Put_change_in_OI'][i] > df['Put_change_in_OI'][i-1]  and df['Put_change_in_OI'][i] > df['Put_change_in_OI'][i+1] and df['Put_change_in_OI'][i] > df['Put_change_in_OI'][i+2] and df['Put_change_in_OI'][i] > df['Put_change_in_OI'][i-2]
    return support2 or support1

'''
Returns a boolean whether the data can be a resistance or not
'''

def isResistance(df,i):
    resistance1 = df['Call_OI'][i] > df['Call_OI'][i-1] and df['Call_OI'][i] > df['Call_OI'][i+1] and df['Call_OI'][i] > df['Call_OI'][i-2] and df['Call_OI'][i] > df['Call_OI'][i+2]
    resistance2 = df['Call_change_in_OI'][i] > df['Call_change_in_OI'][i-1]  and df['Call_change_in_OI'][i] > df['Call_change_in_OI'][i+1] and df['Call_change_in_OI'][i] > df['Call_change_in_OI'][i-2] and df['Call_change_in_OI'][i] > df['Call_change_in_OI'][i+2]
    return  resistance2 or resistance1

'''
Returns a list of top 3 resistances 
'''

def findResistanceLevels(levels):
    resistance = []
    for x in levels:
        if(x[4] > spotprice):
            resistance.append(x)
    return resistance[:3]

'''
Returns a list of top 3 supports 
'''

def findSupportLevels(levels):
    support = []
    for x in levels:
        if(x[4] <= spotprice):
            support.append(x)

    return support[-3:]


'''
Calls the function for fetching NSE data and spotPrice
'''
output = fetch_option_chain.driver('NIFTY','nse')
data = output[0]
spotprice = output[1]

'''
Filters out the obtained data into calls data and puts data based on the fields
'''
dataOfCalls = data[['Call_OI','Call_change_in_OI','Call_total_traded_vol','Call_net_change','StrikePrice']]
dataOfPuts = data[['Put_OI','Put_change_in_OI','Put_total_traded_vol','Put_net_change','StrikePrice']]

'''
Calculates the levels for the calls and puts based on support and resistance
'''
levels = []
for i in range(2,dataOfPuts.shape[0]-2):
    if isSupport(dataOfPuts,i):
        levels.append((i,dataOfPuts['Put_OI'][i],dataOfPuts['Put_change_in_OI'][i],data['Put_net_change'][i],data['StrikePrice'][i]))
    elif isResistance(dataOfCalls,i):
        levels.append((i,dataOfCalls['Call_OI'][i],dataOfCalls['Call_change_in_OI'][i],data['Call_net_change'][i],data['StrikePrice'][i]))

support = findSupportLevels(levels)
resistance = findResistanceLevels(levels)
