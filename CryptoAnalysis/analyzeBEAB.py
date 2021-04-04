import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import seaborn as sns



plt.style.use('Solarize_Light2')


df = pd.read_csv("BEABDatas/main.csv")
df = df.set_index(pd.DatetimeIndex(df['datetime'].values))
df = df.drop(['datetime'],axis=1)



def scale_and_graph(df):

    #We will scale the data frame. Thus we can see cryptocurrencies increasing and decreasing values more detailed

    scaler = preprocessing.MinMaxScaler(feature_range=(0,100))
    scaled = scaler.fit_transform(df)

    df_scaled = pd.DataFrame(scaled,columns=df.columns)
    df_scaled = df_scaled.set_index(pd.DatetimeIndex(df.index))


    #Plotting the graph

    plt.figure(figsize=(15,10))
    for crypto in df_scaled.columns.values:

        plt.plot(df_scaled[crypto],label=crypto)

    plt.title("Cryptocurrency Graph")
    plt.xlabel('Days')
    plt.ylabel('Price $')
    plt.legend(df_scaled.columns.values,loc="upper left")
    plt.show()


    sns.pairplot(df,kind="reg")

scale_and_graph(df)

def daily_simple_return(df,periods):



    return




