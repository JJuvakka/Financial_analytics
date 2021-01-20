



## ---- Goal of this project is to simulate the S&P 500 stock index and to generate portfolio
# simulations for (short) vertical call spread option portfolio. ---- ##

import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
import math


## tradesimulation() returns the following metrics for single (short) vertical call spread position: The probability for profit and the expected value.
# The expected portfoliovalue, the expected annual return and the probabilities for 50 % or 100 % loss are simulated by selling the identical (short) vertical call spread n times.

def tradesimulation(currentindexprice, annualreturn, annualvolatility, K1, K2, daystomaturity, sellingprice, maxloss, periods, startingportfoliovalue) :
    
    all_walks = []

    for i in range(10000) :
        steps = np.random.normal(loc = (1+annualreturn)**(1/365)-1, scale = annualvolatility/math.sqrt(365), size = daystomaturity) + 1
        # First element to 1
        steps[0] = 1
    
        # Simulating stock price P by taking the cumulative product of the daily returns
        P = currentindexprice * np.cumprod(steps)
        all_walks.append(P)

    # Transposing
    all_walks_t = np.transpose(all_walks)

    # Selecting the last price value: ends
    ends = all_walks_t[-1,:]
    
    probabilityforprofit = sum(ends <= K1) / len(ends)
    probabilityforloss = sum(ends >= K2) / len(ends)
    probabilityforhalfloss = (sum(ends < K2) - sum(ends < K1)) / len(ends)
    
    print("Probability for profit is: " + str(probabilityforprofit*100) + " %")
    print("Expected value for the trade is: " + str(probabilityforprofit*sellingprice + probabilityforloss*maxloss + probabilityforhalfloss*((sellingprice+maxloss)/2)))

    # Simulating returns for option portfolio where OTM vertical call spreads are sold x times
    
    portfoliovalue = []
    all_portfoliovalues = []

    for i in range(5000):
        
        # Simulating whether profit or loss occurs
        profitorloss = np.random.choice((sellingprice, maxloss, (sellingprice+maxloss)/2), size = periods, p = [probabilityforprofit, probabilityforloss, probabilityforhalfloss])
        # Steps for portfoliovalue
        portfoliovalue = startingportfoliovalue + np.cumsum(profitorloss)
        # Condition for portfoliovalue dropping to zero
        for n in range(0, len(portfoliovalue)):
            if portfoliovalue[n] <= 0:
                portfoliovalue[n:] = 0
            
        all_portfoliovalues.append(portfoliovalue)
    # Transposing
    all_portfoliovalues_t = np.transpose(all_portfoliovalues)
    # Rolling values to start from 1
    np.roll(all_portfoliovalues_t, 1, 0)
    # Startingvalue in index 0
    all_portfoliovalues_t[0,:] = startingportfoliovalue
    
    # Selecting the last portfoliovalue: endsportfolio
    endsportfolio = all_portfoliovalues_t[-1,:]
    annualizedreturn = (((np.mean(endsportfolio)/startingportfoliovalue)**(1/(daystomaturity*periods)))**365)-1

    print("Expected option portfolio value after " + str(periods) + " months is: " + str(np.mean(endsportfolio)))
    print("Expected annual return is: " + str(annualizedreturn*100) + " %")
    print("Probability for portfolio value to drop 50 % is: " + str(sum(endsportfolio <= 0.5*startingportfoliovalue) / len(endsportfolio) * 100) + " %")
    print("Probability for portfolio value dropping to zero is: " + str(sum(endsportfolio <= 0) / len(endsportfolio) * 100) + " %")
    
    plt.plot(all_portfoliovalues_t)
    plt.xlabel('Period')
    plt.ylabel('Portfoliovalue')
    plt.grid(True)
    plt.title('Simulated portfolio values')
    plt.show()
    plt.figure()
    plt.hist(endsportfolio)
    plt.xlabel('Portfoliovalue')
    plt.title('Histogram of the portfolio values')
 
    
 
    
 
    