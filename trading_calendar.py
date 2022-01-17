import pandas_market_calendars as mcal
import datetime

def GetNumberOfTradingDaysUntilExpiration(optionExpirationDate):
    #calculate number of trading days from now until expiration
    nyse = mcal.get_calendar('NYSE')
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    tradingDays = len(nyse.valid_days(start_date=today,end_date=optionExpirationDate).date)
    #print(f"Number of trading days from today, {today} and option expiration date {optionExpirationDate} is {tradingDays}")
    return tradingDays