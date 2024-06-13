import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import csv

class Portfolio:

    def __init__(self, positions,name) -> None:
        self.positions = positions
        self.name = name

    
    def deposit_cash(self,amount):
        try:
            self.positions["cash"] += amount

        except:
            self.positions["cash"] = amount


    def withdraw_cash(self,amount):

        if amount <= self.positions["cash"]:
            self.positions["cash"] -= amount

        else:
            print("Insufficient funds in account")

    
    def buy_ticker(self,ticker,amount):

        stock = yf.Ticker(ticker)
        price = stock.info["open"]

        if price*amount > self.positions["cash"]:

            print("Insufficient funds in account")

        else:
            self.positions["cash"] -= price*amount

            try:
                self.positions[ticker] += amount
            except:
                self.positions[ticker] = amount

    
    def sell_ticker(self,ticker,amount):

        stock = yf.Ticker(ticker)
        price = stock.info["open"]

        if amount > self.positions[ticker]:

            print("Error - Amount greater than owned")

        else:

            self.positions[ticker] -= amount
            self.positions["cash"] += amount*price

    
    def pie_chart(self):

        total_value, values = self.valuation()

        labels = [x for x in self.positions.keys()]
        percentages = [x/total_value for x in values]

        fig,ax = plt.subplots()
        ax.pie(percentages,labels=labels,autopct='%1.1f%%')
        plt.title(self.name + " Breakdown")
        plt.show()

    
    def valuation(self):

        total_value = 0
        values = []
        for holding in self.positions.keys():

            if holding == "cash":
                total_value += self.positions[holding]
                values.append(self.positions[holding])

            else:

                stock = yf.Ticker(holding)
                price = stock.info["open"]
                total_value += price*self.positions[holding]
                values.append(price*self.positions[holding])

        return total_value,values
    
    def save_positions(self):

        with open(self.name+".csv","a",newline='') as csvfile:

            csvwriter = csv.writer(csvfile)

            csvwriter.writerow([datetime.datetime.now()])
            csvwriter.writerow(self.positions.keys())
            csvwriter.writerow(self.positions.values())

    

        








    
    




    

    

    
