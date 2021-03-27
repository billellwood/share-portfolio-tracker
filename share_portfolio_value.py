import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

todays_date = datetime.datetime.now().date()

os.chdir("/Users/billellwood/Dropbox/My Mac (Williams-MacBook-Pro.local)/Desktop/Programming/Stock_Portfolio")



#series starts from first date stock purchased

class StockTransaction:
    def __init__(self, tkr, units, cost_price, fee, date):
        self.tkr = tkr
        self.units = units
        self.cost_price = cost_price
        self.fee = fee
        self.date = date
        self.total_value = (self.units * self.cost_price) - self.fee
        
    def get_data(self):
        data = yf.download(self.tkr, start = self.date, end = todays_date.strftime('%Y-%m-%d'), 		  interval = "1d")
        data['Holdings value'] = data['Close'] * self.units
        data.loc[self.date, 'Holdings value'] = self.units * self.cost_price - self.fee
        return data
    
    def Buy_Stock(self):
        if os.path.exists("Stocks"):
            records = open("Stocks", "a")
            records.write("\n" + "BUY," + self.tkr + "," + str(self.units) + "," + str(self.cost_price) + "," + str(self.fee) + "," + str(self.date))
        else:
            records = open("Stocks", "w")
            records.write("BUY," + self.tkr + "," + str(self.units) + "," + str(self.cost_price) + "," + str(self.fee) + "," + str(self.date))
            
    def Sell_Stock(self):
        if os.path.exists("Stocks"):
            records = open("Stocks", "a")
            records.write("\n" + "SELL," + self.tkr + "," + str(self.units) + "," + str(self.cost_price) + "," + str(self.fee) + "," + str(self.date))
        else:
            return "Sorry, you need to own this stock before you sell."



class Portfolio:
    
    def __init__(self):
        pass
  
    def Get_All_Transactions(self):
        with open("Stocks", "r") as s:
            each_transaction_in_list = s.readlines()
        return [i.split(",") for i in each_transaction_in_list]
    
    def Get_All_Companies(self):
        companies = [i[1] for i in self.Get_All_Transactions()]
        return list(set(companies))
        
    def Retrieve_Earliest_Date(self):
        transactions = self.Get_All_Transactions()
        all_dates = [datetime.datetime.strptime(i[5][:10],'%Y-%m-%d') for i in transactions]
        return min(all_dates)
    
    def Initialise_Portfolio_DataFrame(self):
        date_index = pd.date_range(self.Retrieve_Earliest_Date(), todays_date, freq="D", )
        weekdays = []
        for i in date_index:
            if i.weekday() < 5:
                weekdays.append(i)
        columns = self.Get_All_Companies()
        df = pd.DataFrame(index=weekdays, columns=columns)
        for i in columns:
            df[i] = df[i].combine_first(List[columns.index(i)]['Holdings value'])
        return df
    
    def Calculate_Final_Holding_Value(self):
        portfolio = self.Initialise_Portfolio_DataFrame()
        portfolio['Total Value'] = portfolio.sum(axis = 1)
        return portfolio
    
    
    
    
BOQ = StockTransaction('BOQ.AX', 200, 12.60, 10, "2015-12-01")
APT = StockTransaction('APT.AX', 200, 5.12, 10, "2017-10-01")
AEF = StockTransaction('AEF.AX', 1000, 1.90, 10, "2019-11-01")

BOQ_stock = BOQ.value_series()[['Holdings value']]
APT_stock = APT.value_series()[['Holdings value']]
AEF_stock = AEF.value_series()[['Holdings value']]

List = [APT_stock, BOQ_stock, AEF_stock]

BOQ.Buy_Stock()
APT.Buy_Stock()
APT.Sell_Stock()
AEF.Buy_Stock()


First_Portfolio = Portfolio()
Transactions = First_Portfolio.Get_All_Transactions()
Earliest_date = First_Portfolio.Retrieve_Earliest_Date()

print(First_Portfolio.Get_All_Companies())
print(First_Portfolio.Initialise_Portfolio_DataFrame())
print(First_Portfolio.Calculate_Final_Holding_Value())
