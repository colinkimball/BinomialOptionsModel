import pandas as pd
import numpy as np
import math
import sys

def GetYangZhangVolatility(price_data):

    #we will use a 5 trading day (1 standard week) window to calculate the rolling volatility over time
    window = 5
    #trading periods is set to a default of 252 since that is the standard number of trading days in a year
    trading_periods = 252
    #get natural log of each fluctuation combination of OHLC - using natural log to make fluctuations more normally distributed
    log_high_open = (price_data['high'] / price_data['open']).apply(np.log)
    log_low_open = (price_data['low'] / price_data['open']).apply(np.log)
    log_close_open = (price_data['close'] / price_data['open']).apply(np.log)
    
    #for open-close, analyze the 'overnight' fluctuation between the open and the previous close
    log_open_close_squared = (price_data['open'] / price_data['close'].shift(1)).apply(np.log)**2
    
    #for close-close, compare the current close to the prior close to account for overnight shift plus day's activity
    log_close_close_squared = (price_data['close'] / price_data['close'].shift(1)).apply(np.log)**2
    
    rs = log_high_open * (log_high_open - log_close_open) + log_low_open * (log_low_open - log_close_open)
    
    close_vol = log_close_close_squared.rolling(
        window=window
    ).sum() * (1.0 / (window - 1.0))
    open_vol = log_open_close_squared.rolling(
        window=window
    ).sum() * (1.0 / (window - 1.0))
    window_rs = rs.rolling(
        window=window
    ).sum() * (1.0 / (window - 1.0))

    k = 0.34 / (1.34 + (window + 1) / (window - 1))
    result = (open_vol + k * close_vol + (1 - k) * window_rs).apply(np.sqrt) * math.sqrt(trading_periods)

    return result.dropna()
    


def CreateHistoricalOHLCDataframe(historicalData):
    date = []
    open = []
    high = []
    low = []
    close = []
    volume = []

    for item in historicalData.items():
        date.append(item[0])
        open.append(float(item[1]['1. open']))
        high.append(float(item[1]['2. high']))
        low.append(float(item[1]['3. low']))
        close.append(float(item[1]['4. close']))
        volume.append(float(item[1]['5. volume']))

    dataframe = pd.DataFrame(data={'date': date, 'open': open, 'high': high, 'low': low, 'close': close, 'volume': volume})
    dataframe['daily_range_percent'] = abs((dataframe['high'] - dataframe['low']) / dataframe['low'])
    dataframe['closing_percent_change'] = (dataframe['close'] - dataframe['open']) / dataframe['open']
    dataframe['daily_change'] = dataframe['close'] - dataframe['open']

    return dataframe

def GetVolatilityMetrics(historicalData,riskFreeRate):
    selectionNumber = input("""
    Choose your volatility calculation methodology:
    1. Yang-Zhang formula - based on Open-High-Low-Close historical price data
    2. Manual User Input (expressed as annual implied volatility; 60% = 60)
    
    """)
    historicalPriceData = CreateHistoricalOHLCDataframe(historicalData)
    if selectionNumber == "1":
        volatilityNpArray = GetYangZhangVolatility(historicalPriceData)
        dailyVolatility = volatilityNpArray.mean()/252  
    # volatility of asset: propose using standard deviation of closing_percent_change
    elif selectionNumber == "2":
        impliedVolatility = float(input("Enter implied volatility: "))
        dailyVolatility = impliedVolatility/100/252
    
    percentUp = (len(historicalPriceData[historicalPriceData['daily_change']>0])/len(historicalPriceData))
    alternativePercentUp = (np.exp(riskFreeRate/100/252) - (1/(1+dailyVolatility))) / ((1+dailyVolatility) - (1-dailyVolatility))

    return dailyVolatility, alternativePercentUp



