import requests
import api_key
apiKey = api_key.apiKey
quoteFunction = "GLOBAL_QUOTE"
timeSeriesFunction = "TIME_SERIES_DAILY"


def AlphaInsightsAPIRequest(function, symbol, apiKey):
    url = f"https://www.alphavantage.co/query?function={function}"
    url += f"&symbol={symbol}"
    url += f"&apikey={apiKey}"
    request = requests.get(url)
    data = request.json()
    return data

def GetHistoricalData(symbol):
    historicalData = dict(AlphaInsightsAPIRequest(timeSeriesFunction,symbol,apiKey)['Time Series (Daily)'])
    return historicalData

def GetCurrentPrice(symbol):
    currentPrice = float(AlphaInsightsAPIRequest(quoteFunction,symbol,apiKey)['Global Quote']['05. price'])
    return currentPrice