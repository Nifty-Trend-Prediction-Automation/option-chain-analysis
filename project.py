from fetch_option_chain import *
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

def findResistanceLevels(levels, spotprice):
    resistance = []
    for x in levels:
        if(x[4] > spotprice):
            resistance.append(x)
    return resistance[:3]

'''
Returns a list of top 3 supports 
'''

def findSupportLevels(levels, spotprice):
    support = []
    for x in levels:
        if(x[4] <= spotprice):
            support.append(x)

    return support[-3:]




def fetch_support_resistance_levels():
    '''
    Calls the function for fetching NSE data and spotPrice
    '''
    output = driver('NIFTY','nse')
    data, spotprice = output[0], output[1]

    '''
    Filters out the obtained data into calls data and puts data based on the fields
    '''
    dataOfCalls = data[['Call_OI','Call_change_in_OI','Call_total_traded_vol','Call_net_change','StrikePrice', 'Call_total_traded_vol']]
    dataOfPuts = data[['Put_OI','Put_change_in_OI','Put_total_traded_vol','Put_net_change','StrikePrice', 'Put_total_traded_vol']]

    '''
    Calculates the levels for the calls and puts based on support and resistance
    '''
    levels = []
    for i in range(2,dataOfPuts.shape[0]-2):
        if isSupport(dataOfPuts,i):
            levels.append([i,dataOfPuts['Put_OI'][i],dataOfPuts['Put_change_in_OI'][i],data['Put_net_change'][i],data['StrikePrice'][i], data['Put_total_traded_vol'][i]])
        elif isResistance(dataOfCalls,i):
            levels.append([i,dataOfCalls['Call_OI'][i],dataOfCalls['Call_change_in_OI'][i],data['Call_net_change'][i],data['StrikePrice'][i], data['Call_total_traded_vol'][i]])

    support = findSupportLevels(levels, spotprice)
    resistance = findResistanceLevels(levels, spotprice)
    # print(spotprice)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(data)
    return (support, resistance)


def get_num(levels):

    val = list()
    for i in levels: 
        if i[3] < 0 and i[2] < 0:
            val.append(-1)
        elif i[3] < 0 and i[2] > 0:
            val.append(-1)
        elif i[3] > 0 and i[2] > 0:
            val.append(1)
        else:
            val.append(1)

    return val

def predict_market_trend():
    (support, resistance) = fetch_support_resistance_levels()
    sup = get_num(support)
    res = get_num(resistance)

    priority = [0.5, 0.3, 0.2]

    final_val = 0
    for i in range(3):
        final_val += (sup[i]+res[i])*priority[i]

    if final_val >=0:
        return 'Bullish'
    else:
        return 'Bearish'
    
print(predict_market_trend())