# Script for testing new yfinance implementation.
from async_finance import Finance

print("Starting finance data service")
finance = Finance()
finance.thread.join()