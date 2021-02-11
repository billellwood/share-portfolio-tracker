import yfinance as yf
import pandas as pd
import numpy as pd
import matplotlib.pyplot as plt
from datetime import date

stocks = ['APT.AX', 'BOQ.AX', 'VDHG.AX']


#series starts from first date stock purchased

class Stock:
    def __init__(self, tkr, units, cost_price, fee, date):
        self.tkr = tkr
        self.units = units
        self.cost_price = cost_price
        self.fee = fee
        self.date = date
        self.total_value = (self.units * self.cost_price) - self.fee

    def movements(self):
        data = yf.download(self.tkr, start = self.date, end = date.today().strftime('%Y-%m-%d'), interval = "1d")
        data['Movement'] = data['Close'].pct_change()
        return data
    
    def value_series(self):
        data = self.movements()
        data['Holdings value'] = data['Adj Close'] * self.units
        data.loc['2017-12-01', 'Holdings value'] = self.units * self.cost_price - self.fee
        print(data.head())
        #data['Holdings value'][0] = self.units * self.cost_price - self.fee
        return data
 

BOQ = Stock('VDHG.AX', 200, 50, 10, "2015-12-01")
APT = Stock('BOQ.AX', 200, 5.12, 10, "2017-10-01")

portfolio_value = BOQ.value_series()[['Holdings value']]
print(portfolio_value.head())
portfolio_value['APT Holding value'] = APT.value_series()[['Holdings value']]
portfolio_value.fillna(0, inplace = True)
portfolio_value['Total value'] = portfolio_value['Holdings value'] + portfolio_value['APT Holding value']
print(portfolio_value.head())
portfolio_value['Total value'].plot()


            




    
    
    
    
    
    