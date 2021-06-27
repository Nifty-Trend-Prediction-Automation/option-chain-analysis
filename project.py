import fetch_option_chain
import pandas as pd
import numpy as np

def isSupport(df,i):
    support1 = df['Put_OI'][i] < df['Put_OI'][i-1]  and df['Put_OI'][i] < df['Put_OI'][i+1] and df['Put_OI'][i+1] < df['Put_OI'][i+2] and df['Put_OI'][i-1] < df['Put_OI'][i-2]
    support2 = df['Put_change_in_OI'][i] < df['Put_change_in_OI'][i-1]  and df['Put_change_in_OI'][i] < df['Put_change_in_OI'][i+1] and df['Put_change_in_OI'][i+1] < df['Put_change_in_OI'][i+2] and df['Put_change_in_OI'][i-1] < df['Put_change_in_OI'][i-2]
    return support2 or support1

def isResistance(df,i):
    resistance1 = df['Call_OI'][i] > df['Call_OI'][i-1] and df['Call_OI'][i] > df['Call_OI'][i+1] and df['Call_OI'][i+1] > df['Call_OI'][i+2] and df['Call_OI'][i-1] > df['Call_OI'][i-2]
    resistance2 = df['Call_change_in_OI'][i] > df['Call_change_in_OI'][i-1]  and df['Call_change_in_OI'][i] > df['Call_change_in_OI'][i+1] and df['Call_change_in_OI'][i+1] > df['Call_change_in_OI'][i+2] and df['Call_change_in_OI'][i-1] > df['Call_change_in_OI'][i-2]
    return  resistance2 or resistance1

def isFarFromLevel(l,s,levelsForOI):
    if(l != '-'):
        for x in levelsForOI:
            return np.sum([abs(l-x) > s  for x in levelsForOI]) == 0

def cleanTheNoiceForPuts(df):
    s1 = 0
    for x in df['Put_OI']:
        if(x != "-"):
            s1=s1+x

    s2 = 0
    for x in df['Put_change_in_OI']:
        if(x != "-"):
            s1=s1+x

    return (s1-s2)/df.shape[0]

def cleanTheNoiceForCalls(df):
    s1 = 0
    for x in df['Call_OI']:
        if(x != "-"):
            s1=s1+x
    s2 = 0
    for x in df['Call_change_in_OI']:
        if(x != "-"):
            s1=s1+x

    return (s1-s2)/df.shape[0]


data = fetch_option_chain.driver('NIFTY')
print(data.columns)

dataOfCalls = data[['Call_OI','Call_change_in_OI','Call_total_traded_vol','StrikePrice']]

dataOfPuts = data[['Put_OI','Put_change_in_OI','Put_total_traded_vol','StrikePrice']]

spotprice = 15680

dataOfCalls= dataOfCalls[dataOfCalls['StrikePrice'] > spotprice]

dataOfPuts= dataOfPuts[dataOfPuts['StrikePrice'] < spotprice]

# print(dataOfCalls)

# print(dataOfPuts)


levelsForOI = []
for i in range(2,dataOfPuts.shape[0]-2):
    if isSupport(dataOfPuts,i):
        levelsForOI.append((i,dataOfPuts['Put_OI'][i],dataOfPuts['Put_change_in_OI'][i],data['StrikePrice'][i]))
        print("ts")
print(levelsForOI)

levelsForOI = []
for i in range(2,dataOfCalls.shape[0]-2):
    if isResistance(dataOfCalls,i):
        levelsForOI.append((i,dataOfCalls['Call_OI'][i],dataOfCalls['Call_change_in_OI'][i], data['StrikePrice'][i]))
        print("ts1")

print(levelsForOI)

# s = cleanTheNoiceForCalls(dataOfCalls)+ cleanTheNoiceForPuts(dataOfPuts)
# s = s//2
# print(s)

# levels = []
# support = []
# resistance = []
# for i in range(2,data.shape[0]-2):
#     if isSupport(dataOfPuts,i):
#         print("ks")
#         l1 = dataOfPuts['Put_OI'][i]
#         l2 = dataOfPuts['Put_change_in_OI'][i]
#         if isFarFromLevel(l1,s,levelsForOI) or isFarFromLevel(l2,s,levelsForOI):
#             levels.append((i,dataOfPuts['Put_OI'][i],dataOfPuts['Put_change_in_OI'][i],data['StrikePrice'][i]))
#             support.append((i,dataOfPuts['Put_OI'][i],dataOfPuts['Put_change_in_OI'][i],data['StrikePrice'][i]))
#             print("ls")
#     elif isResistance(dataOfCalls,i):
#         l1 = dataOfCalls['Call_OI'][i]
#         l2 = dataOfCalls['Call_change_in_OI'][i]
#         print("ks1")
#         if isFarFromLevel(l1,s,levelsForOI) or isFarFromLevel(l2,s,levelsForOI):
#             levels.append((i,dataOfCalls['Call_OI'][i],dataOfCalls['Call_change_in_OI'][i], data['StrikePrice'][i]))
#             resistance.append((i,dataOfCalls['Call_OI'][i],dataOfCalls['Call_change_in_OI'][i], data['StrikePrice'][i]))
#             print("ls1")

# print(support)
# print(resistance)
# temp = 0
# for x in range(dataOfCalls.shape[0]):
#     if(data['StrikePrice'][x] > 15860 ):
#         temp = x
#         break
# dataOfCalls = dataOfCalls[temp+1:,:]
# dataOfPuts = dataOfPuts[:temp,:]
# print(dataOfCalls)
# print(dataOfPuts)
