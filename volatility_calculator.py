import pandas as pd

def GetVolatilityMetrics(historicalData):
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
    #print(dataframe[['daily_range_percent', 'closing_percent_change']].describe())

    # volatility of asset: propose using standard deviation of closing_percent_change
    volatility = dataframe['closing_percent_change'].std()
    percentUp = (len(dataframe[dataframe['daily_change']>0])/len(dataframe))

    return volatility, percentUp
