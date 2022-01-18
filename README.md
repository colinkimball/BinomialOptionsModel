# Binomial Options Model
This project provides a transparent, modular, and adjustable binomial options valuation model for call stock options.
There are a number of free online tools available that will model the pricing of stock options, however they are often non-transparent
and non-adjustable regarding the underlying assumptions and methodologies behind the valuations.


## Visual Representation
The below chart shows how options are valued using binomial model. 
We start at Time 0, where S<sub>0</sub> is equal to current stock price. For each trading day, there is a ***p*** likelihood that the stock price
will close ***u*** higher, and a 1 - ***p*** likelihood that it will close ***d*** lower.
The daily changes compound each trading day until we arrive at the option expiry date. On the option expiry date, the value of the call option is equal to 
the greater of zero or the strike price less the current stock price (ie, the intrinsic value of the option). Once given this value as of the expiry date, the model
will step back in time, discounting using the risk free rate, until arriving back at Time 0 with a modeled valuation (a combination of intrinsic value and time value).

![alt text](https://marketxls.com/wp-content/uploads/2020/07/1.gif)

## Key Inputs and Assumptions

### Current Stock Price
The current stock price is retrieved from [Alpha Vantage's Rest API service](https://www.alphavantage.co/documentation/) given the User's input.

### Daily Volatility and Likelihood Closing Higher (to be refined)
The program uses Alpha Vantage's Rest API service to retrieve the daily price experience (open, high, low, close) for the last 100 trading days, and creating a Pandas dataframe of this information.
It currently takes a simple percentage calculation of the number of trading days closed higher versus lower. 

The daily expected volatility is currently calculated by taking the standard deviation of 100 days of the percent change between the open and closing price. This will be expanded
and refined significantly with multiple options for the user to choose.

### Risk Free Rate
The user has four options to use as the Risk Free Rate: the 10 Year US Treasury Yield, the current Federal Funds Rate, the current USD Inflation Rate, and finally a manual user input.
The first three items are retrieved from AlphaVantage's rest API service as of the most recent trading day.

### Number of Trading Days Until Expiration
The program uses the [pandas-market-calendar](https://pypi.org/project/pandas-market-calendars/) library to calculate the number of trading days between Time 0 (today) and the option expiration date.
The calendar is based on the active trading days as listed by the New York Stock Exchange.
