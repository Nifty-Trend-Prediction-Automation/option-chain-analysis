from fetch_option_chain import *
import pandas as pd

def is_peak(df, i, col1):
    return ((df[col1][i] > df[col1][i-1])  or (df[col1][i] > df[col1][i+1])) #or (df[col1][i] > df[col1][i-1]) or (df[col1][i]>df[col1][i+1])

def get_peaks(df, col):
    peaks = list()
    for i in range(2, df.shape[0]-2):
        if is_peak(df, i, col):
            peaks.append(df.iloc[i])
    return pd.DataFrame(peaks, columns = df.columns)

def get_keys(df, spotprice):
    df1 = df[df['StrikePrice']<=spotprice].tail(3)
    df2 = df[df['StrikePrice']>spotprice].head(3)
    df = pd.concat([df1, df2])
    return df.values.tolist()
'''
 ['Call_OI', 'Call_change_in_OI','Call_total_traded_vol', 'Call_net_change', 'StrikePrice', 'Put_net_change', 'Put_total_traded_vol', 'Put_change_in_OI', 'Put_OI']
'''
def get_supp_num(levels):
    
    level_priority = [0.025, 0.075, 0.4, 0.4, 0.075, 0.025]
    gran = [0.2, 0.2, 0.6]
    score = 0

    state = []
    values = []

    for level in levels:
        if level[5] >= 0 and level[-2] >= 0:
            # BEARISH
            state.append(-1)
        elif level[5] < 0 and level[-2] >= 0:
            # BULLISH
            state.append(1)
        elif level[5] >=0 and level[-2] < 0:
            # WEAKLY BEARISH
            state.append(-0.5)
        else:
            # WEAKLY BULLISH
            state.append(+0.5)
    
    for i in range(len(levels)):
        
        level = levels[i]

        level_score = level[6]*gran[0] + level[7]*gran[1] + level[8]*gran[2]
        level_score *= level_priority[i] * state[i]

        score += level_score

    # print(score)
    return score


def get_resis_num(levels):
    
    level_priority = [0.025, 0.075, 0.4, 0.4, 0.075, 0.025]
    gran = [0.2, 0.2, 0.6]
    score = 0

    state = []
    values = []

    for level in levels:
        if level[5] >= 0 and level[-2] >= 0:
            # BEARISH
            state.append(1)
        elif level[5] < 0 and level[-2] >= 0:
            # BULLISH
            state.append(-1)
        elif level[5] >=0 and level[-2] < 0:
            # WEAKLY BEARISH
            state.append(+0.5)
        else:
            # WEAKLY BULLISH
            state.append(-0.5)
    
    for i in range(len(levels)):
        
        level = levels[i]

        level_score = level[6]*gran[0] + level[7]*gran[1] + level[8]*gran[2]
        level_score *= level_priority[i] * state[i]

        score += level_score
    # print(score)
    return score


def fetch_support_resistance_levels():
    data, spotprice = driver('NIFTY','nse')
    support_peaks = get_peaks(data, 'Put_OI')
    resistance_peaks = get_peaks(data, 'Call_OI')
    support_key_levels  = get_keys(support_peaks, spotprice)
    resistance_key_levels = get_keys(resistance_peaks, spotprice)
    print(support_key_levels)
    print(resistance_key_levels)
    snum = get_supp_num(support_key_levels)
    rnum = get_resis_num(resistance_key_levels)
    print(spotprice)
    print(snum, rnum)

fetch_support_resistance_levels()