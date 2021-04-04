"""
@author: sarperyurtseven
"""

import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from requests.api import request
import os


"""

### Functions

   * save_200_cryptocurrency : this function gets top 200 cryptocurrencies symbols from coinmarketcap.com using BeautifulSoup
   
      
  
   * get_filename : this function gets name of our csv files which we're gonna get for each coin and our format is something like this --> BTC_USD_Binance_day_2021-03-13
   
   
   * download_data : downloading data using cryptocompare API
   
   
   * convert_to_dataframe : the datas come to us in json format. we convert these to pandas dataframe.
   
   
   * save_datas : saving datas as csv file.
   
"""


def save_200_cryptocurrency():
    
    resp = requests.get('https://coinmarketcap.com/all/views/all/')
    soup = BeautifulSoup(resp.text,'lxml')
    
    symbolsHtml = soup.findAll('td',class_="cmc-table__cell--sort-by__symbol")
    symbols = [symbol.text for symbol in symbolsHtml]
    
    with open('top_200_cryptocurrency.txt','r') as file:
        file.writelines(f'{symbol}\n' for symbol in symbols)

    return symbols   



#symbolList = save_200_cryptocurrency()




def get_filename(symbol,to_symbol,exchange,datetime_interval,download_date):
    
    return '%s_%s_%s_%s_%s.csv' % (symbol, 
                                   to_symbol, 
                                   exchange, 
                                   datetime_interval, 
                                   download_date)




def download_data(symbol,to_symbol,exchange,datetime_interval):

    supported_intervals = {'minute','hour','day'}

    assert datetime_interval in supported_intervals,\
        'datetime_interval should be one of %s' % supported_intervals

    print('Downloading %s trading data for %s %s from %s' % (datetime_interval,symbol,to_symbol,exchange))

    download_date = datetime.now().date().isoformat()


    if not os.path.exists("RawDatas"):
        os.mkdir('RawDatas')

    if not os.path.exists("RawDatas/%s_%s_%s_%s_%s.csv" % (symbol,
                                                            to_symbol, 
                                                            exchange, 
                                                            datetime_interval, 
                                                            download_date)):

        try:

            base_url = 'https://min-api.cryptocompare.com/data/histo'
            url = '%s%s' %(base_url,datetime_interval)
            params = { 'fsym':symbol,'tsym':to_symbol,
                        'limit':2000,'aggregate':1}
            request = requests.get(url=base_url,params=params)
            data = request.json()
            print(f'We got {symbol}')
            return data

        except:
            print(f"There is a problem with {symbol}")


def convert_to_dataframe(data):

    df = pd.json_normalize(data,['Data'])
    df['datetime'] = pd.to_datetime(df.time,unit='s')
    df = df[['datetime','low','high','open','close','volumefrom','volumeto']]


    #Filtering empty data points
    indices = df[df.sum(axis=1) == 0 ].index
    print(" Filtering %d empty datapoints " % indices.shape[0])
    df = df.drop(indices)

    return df


def save_datas(to_symbol,exchange,datetime_interval):

    for symbol in symbolList:

        data = download_data(symbol,to_symbol,exchange,datetime_interval)


        if data is not None:

            df = convert_to_dataframe(data)
            df = filter_empty_datapoints(df)


            current_datetime = datetime.now().date().isoformat()
            filename = get_filename(symbol,to_symbol,exchange,datetime_interval,current_datetime)
            df.to_csv(os.path.join("RawDatas/",filename),index=False)


        else:
            continue

#save_datas(to_symbol="USD",exchange='Binance',datetime_interval='day')