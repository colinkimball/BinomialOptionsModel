import pandas as pd
import numpy as np
import math

def GetYangZhangVolatility(price_data, window, trading_periods, clean):

    log_ho = (price_data['high'] / price_data['open']).apply(np.log)
    log_lo = (price_data['low'] / price_data['open']).apply(np.log)
    log_co = (price_data['close'] / price_data['open']).apply(np.log)
    
    log_oc = (price_data['open'] / price_data['close'].shift(1)).apply(np.log)
    log_oc_sq = log_oc**2
    
    log_cc = (price_data['close'] / price_data['close'].shift(1)).apply(np.log)
    log_cc_sq = log_cc**2
    
    rs = log_ho * (log_ho - log_co) + log_lo * (log_lo - log_co)
    
    close_vol = log_cc_sq.rolling(
        window=window,
        center=False
    ).sum() * (1.0 / (window - 1.0))
    open_vol = log_oc_sq.rolling(
        window=window,
        center=False
    ).sum() * (1.0 / (window - 1.0))
    window_rs = rs.rolling(
        window=window,
        center=False
    ).sum() * (1.0 / (window - 1.0))

    k = 0.34 / (1.34 + (window + 1) / (window - 1))
    result = (open_vol + k * close_vol + (1 - k) * window_rs).apply(np.sqrt) * math.sqrt(trading_periods)
    
    if clean:
        return result.dropna()
    else:
        return result


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

def GetVolatilityMetrics(historicalData,riskFreeRate,tradingDays):
    selectionNumber = input("""
    Choose your volatility calculation methodology:
    1. Yang-Zhang formula - based on Open-High-Low-Close historical price data
    2. Manual User Input (expressed as annual implied volatility; 60% = 60)
    
    """)
    historicalPriceData = CreateHistoricalOHLCDataframe(historicalData)
    if selectionNumber == "1":

        volatilityNpArray = GetYangZhangVolatility(historicalPriceData,tradingDays,len(historicalPriceData),True)
        dailyVolatility = volatilityNpArray.mean()/len(volatilityNpArray)    
    # volatility of asset: propose using standard deviation of closing_percent_change
    elif selectionNumber == "2":
        impliedVolatility = float(input("Enter implied volatility: "))
        dailyVolatility = impliedVolatility/100/252
    
    percentUp = (len(historicalPriceData[historicalPriceData['daily_change']>0])/len(historicalPriceData))
    alternativePercentUp = (np.exp(riskFreeRate/100/252) - (1/(1+dailyVolatility))) / ((1+dailyVolatility) - (1-dailyVolatility))

    return dailyVolatility, alternativePercentUp



