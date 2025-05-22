import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# Function to retrieve and process historical stock data
def get_data(stocks, start, end):
    # Download closing price data for the selected stocks within the time range
    stock_data = yf.download(stocks, start=start, end=end)['Close'] 
    
    # Calculate daily percentage returns for each stock
    returns = stock_data.pct_change()
    
    # Calculate the average daily return for each stock
    mean_returns = returns.mean()
    
    # Compute the covariance matrix of stock returns (risk modeling)
    cov_matrix = returns.cov()
    return mean_returns, cov_matrix


#Define the tickers
stockList = ['CBA', 'BHP', 'NAB', 'WBC', 'STO']

# Append '.AX' for format compatiblity (Yahoo Finance)
stocks = [stock + '.AX' for stock in stockList]

#Define date range
end_date = dt.datetime.now()
start_date = end_date - dt.timedelta(days=300)

# Compute the mean returns and the covariance matrix
mean_returns, cov_matrix = get_data(stocks, start_date, end_date)

# Randomly generate portfolio weights (per stock)
weights = np.random.random(len(mean_returns))
# Normalize weights so that sum of all weights = 1
weights /= np.sum(weights) 

# Number of Simulations
sims = 100 
# Forecast Range (Days)
T = 365 

# Compute a matrix with the same daily mean return for each day
meanM = np.full(shape=(T, len(weights)), fill_value=mean_returns)
# Transpose 
meanM = meanM.T

# Initialize a matrix to store simulated portfolio values
portfolio_sims = np.full(shape=(T, sims), fill_value=0.0)

initial_portfolio = 100000 # Starting value of the portfolio (Dollars $)

# MONTE CARLO SIMULATIONS
for m in range(0, sims):
    # Create T X N random standard normal values (N = number of weights(assests))
    Z = np.random.normal(size=(T, len(weights)))
    # Perform Cholesky decomposition on the covariance matrix
    L = np.linalg.cholesky(cov_matrix)
    # Generate correlated daily returns using the Cholesky matrix
    daily_returns = meanM + np.inner(L, Z)
    # Calculate cumulative portfolio value over time
    portfolio_sims[:,m] = np.cumprod(np.inner(weights, daily_returns.T) + 1) * initial_portfolio


# Plot the results    
plt.plot(portfolio_sims)
plt.ylabel('Portfolio Value ($)')
plt.xlabel('Days')
plt.title('ManteCarlo simulation of a stock portfolio')
plt.show()



