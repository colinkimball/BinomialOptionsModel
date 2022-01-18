import risk_free_rate
import trading_calendar
import api_params
import volatility_calculator
import binomial_tree_model

symbol = input("Enter the stock symbol: ")
optionStrikePrice = float(input("Enter the call option strike price: "))
optionExpirationDate = input("Enter the call option expiration date (YYYY-MM-DD): ")


tradingDays = trading_calendar.GetNumberOfTradingDaysUntilExpiration(optionExpirationDate)
currentPrice = api_params.GetCurrentPrice(symbol)
riskFreeRate = risk_free_rate.GetRiskFreeRate()
historicalData = api_params.GetHistoricalData(symbol)
volatility, percentUp = volatility_calculator.GetVolatilityMetrics(historicalData,riskFreeRate,tradingDays)


modeledOptionValue = binomial_tree_model.BinomialTreeOptionValuationModel(tradingDays,currentPrice,volatility,percentUp,optionStrikePrice,riskFreeRate)
print(f"The modeled value of {symbol} ${optionStrikePrice} calls expiring {optionExpirationDate} is ${modeledOptionValue}")
print(f"This is based on the assumption of a risk free rate of {round(riskFreeRate,3)}%, expected daily volatility of {round(volatility*100,2)}%, and a {percentUp*100}% expected chance of a daily positive return")