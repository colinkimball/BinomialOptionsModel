import requests
import api_params

def GetRiskFreeRate():
    selectionNumber = input("""
    Select your risk free rate assumption. Options are:
    1. 10 Year Treasury Rate
    2. Monthly Federal Funds Rate
    3. Current Inflation Rate
    4. Manual User Input (expressed as percentage; 1% = 1)
    """)
    if selectionNumber == "1":
        url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD"
        url +=f"&interval=daily&maturity=10year&apikey={api_params.apiKey}"
        request = requests.get(url)
        data = request.json()
        currentYield = float(data['data'][0]['value'])
        return currentYield
    elif selectionNumber == "2":
        url = f"https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE"
        url +=f"&interval=monthly&apikey={api_params.apiKey}"
        request = requests.get(url)
        data = request.json()
        fundsRate = float(data['data'][0]['value'])
        return fundsRate
    elif selectionNumber == "3":
        url = f"https://www.alphavantage.co/query?function=INFLATION"
        url +=f"&apikey={api_params.apiKey}"
        request = requests.get(url)
        data = request.json()
        inflation = float(data['data'][0]['value'])
        return inflation
    elif selectionNumber == "4":
        rate = float(input("Manually enter risk free rate: "))
        return rate
