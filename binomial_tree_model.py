import numpy as np

def BinomialTreeOptionValuationModel(tradingDays,currentPrice,volatility,percentUp,optionStrikePrice,riskFreeRate):
    #initialize the empty matrix of nodes
    binomialTree = np.zeros([tradingDays+1,tradingDays+1])
    up = 1 + volatility
    down = 1 / up
    percentDown = 1 - percentUp

    for column in range(tradingDays+1):
        for row in range(column+1):
            binomialTree[row, column] = currentPrice * (up ** (column - row)) * (down ** row)

    #print(binomialTree)

    option = np.zeros([tradingDays + 1, tradingDays + 1])
    option[:, tradingDays] = np.maximum(np.zeros(tradingDays + 1), (binomialTree[:, tradingDays] - optionStrikePrice))
    for i in range(tradingDays - 1, -1, -1):
        for j in range(0, i + 1):
            option[j, i] = (
                1 / (1 + (riskFreeRate/100/365)) * (percentUp * option[j, i + 1] + percentDown * option[j + 1, i + 1])
            )
    #print(option)

    return round(option[0][0],2)