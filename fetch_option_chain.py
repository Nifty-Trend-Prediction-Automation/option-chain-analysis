import requests
import requests.exceptions
import api_details

import pandas

'''
Fetches Option chain data from NSEINDIA using official nse API and returns the data in json format
'''

def fetch_json(symbol, underlying_asset):
    
    try:
        
        headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        }

        params = {'symbol': symbol}
        url = api_details.api.get(underlying_asset).get('url')
        method = api_details.api.get(underlying_asset).get('method')
        return requests.request(method, url, headers=headers, params=params).json()

    except requests.exceptions.ConnectionError as ex:
        print('Error Establishing connection with NSE')
        raise SystemError(ex)


'''
Fetches (Data Frame) data relevant to desired expiry date from the provided JSON option_chain data consisting of various expiry date based options
'''
def date_filter(option_chain_data, date):
    
    '''
    Return data format - [Call_OI, Call_change_in_OI, Call_total_traded_vol, StrikePrice, Put_total_traded_vol, Put_change_in_OI, Put_OI]
    '''
    
    column_names = ['Call_OI', 'Call_change_in_OI','Call_total_traded_vol', 'StrikePrice', 'Put_total_traded_vol', 'Put_change_in_OI', 'Put_OI']
    empty_contract = [0,0,0]
    filtered_data = list()


    for dict in option_chain_data.get('records').get('data'):
        if dict.get('expiryDate') == date:
            option_row = list()
            
            if dict.get('CE'):
                call_row = dict.get('CE')
                option_row.append(call_row.get('openInterest'))
                option_row.append(call_row.get('changeinOpenInterest'))
                option_row.append(call_row.get('totalTradedVolume'))
            else:
                option_row += empty_contract
            
            option_row.append(dict.get('strikePrice'))

            if dict.get('PE'):
                put_row = dict.get('PE')
                option_row.append(put_row.get('totalTradedVolume'))
                option_row.append(put_row.get('changeinOpenInterest'))
                option_row.append(put_row.get('openInterest'))
            else:
                option_row += empty_contract

            filtered_data.append(option_row)
    
    df = pandas.DataFrame(data=filtered_data, columns=column_names)
    return df

def get_expiry_dates(option_chain_data):
    return option_chain_data.get('records').get('expiryDates')

'''
Main function that initaiates required function calls
'''
def driver(symbol, underlying_asset):

    ocd = fetch_json(symbol,underlying_asset)
    expiry_dates_available = get_expiry_dates(ocd)
    data = date_filter(ocd, expiry_dates_available[0])
    print(data)

if __name__ == "__main__":
    driver('NIFTY', "nse")





