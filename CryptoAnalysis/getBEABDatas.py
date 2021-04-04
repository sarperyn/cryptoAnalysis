import numpy as np
import pandas as pd
import sqlite3


def prepare_dataframe():

    btc_df = pd.read_csv("RawDatas/BTC_USD_Binance_day_2021-03-13.csv")
    eth_df = pd.read_csv("RawDatas/ETH_USD_Binance_day_2021-03-13.csv")
    ada_df = pd.read_csv("RawDatas/ADA_USD_Binance_day_2021-03-13.csv")
    bnb_df = pd.read_csv("RawDatas/BNB_USD_Binance_day_2021-03-13.csv")

    df_lengths = []

    df_lengths.append(btc_df.shape[0])
    df_lengths.append(eth_df.shape[0])
    df_lengths.append(ada_df.shape[0])
    df_lengths.append(bnb_df.shape[0])

    df_lengths_c = df_lengths.copy()
    df_lengths.sort()

    start = df_lengths[0]
    
    df_lengths_c = [x - start for x in df_lengths_c]
    
    #with order
    btc_df = btc_df.loc[df_lengths_c[0]:]
    eth_df = eth_df.loc[df_lengths_c[1]:]
    ada_df = ada_df.loc[df_lengths_c[2]:]
    bnb_df = bnb_df.loc[df_lengths_c[3]:]


    btc_df.to_csv("BEABDatas/BTC.csv",index=False)
    eth_df.to_csv("BEABDatas/ETH.csv",index=False)
    ada_df.to_csv("BEABDatas/ADA.csv",index=False)
    bnb_df.to_csv("BEABDatas/BNB.csv",index=False)


def get_main_csv():

    conn = sqlite3.connect('crypto.db')

    main_df = pd.read_sql_query(
    """
    Select BTC.datetime,BTC.close AS BTC, ETH.close AS ETH, ADA.close AS ADA, BNB.close AS BNB 
    FROM BTC
    LEFT JOIN ETH on BTC.datetime = ETH.datetime
    LEFT JOIN ADA on ETH.datetime = ADA.datetime
    LEFT JOIN BNB on ADA.datetime = BNB.datetime
    ORDER BY BTC.datetime

    """,conn)

    df = pd.DataFrame(main_df)
    df.to_csv('BEABDatas/main.csv',index=False)

prepare_dataframe()
get_main_csv()