import yfinance as YahooFin
import numpy as np
import matplotlib.pyplot as plt
import csv

# individual positions taken by user
class Position:
    def __init__(self, product, amount, purchase_price):
        self.product= product
        self.amount = amount
        self.purchase_price = purchase_price

    def profit_loss(self):
        ticker = YahooFin.Ticker(self.product)
        current_price = ticker.info['regularMarketPrice']
        profit_loss = self.amount*(current_price - self.purchase_price)
        return profit_loss

    def percentage_change(self):
        ticker = YahooFin.Ticker(self.product)
        current_price = ticker.info['regularMarketPrice']
        if self.purchase_price > current_price:
            return (-1+(current_price/self.purchase_price))
        else:
            return 1- (self.purchase_price/current_price)

# read data from csv file containg positions.
file = "assets.csv"
positions = []
try:
    with open(file,"r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            positions.append(Position(row[0],row[1],row[2]))
except:
    pass

#main program loop
def main():

    # Main input section
    user_input=input("Type '-info [ticker]' to get general information" + "\n" + "Type -graph [ticker] [time range] to get a price graph for times: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y and ytd." + "\n" + "Type -open [ticker] [amount] to buy or sell"+ "\n" +"Type -exit to end the program" )

    # For general infromation
    if user_input[0:5]=="-info":
        get_ticker_info = YahooFin.Ticker(user_input[6::])
        general_stock_info(get_ticker_info)

    # For plotting
    elif user_input[0:6]=="-graph":
        ticker_range_string = user_input[7::] # Splitting string to detect ticker and time range
        ticker_string = ticker_range_string.partition(" ")[0]
        ticker = YahooFin.Ticker(ticker_string)
        time_range = ticker_range_string.partition(" ")[2]
        price_graph(ticker, time_range,ticker_string)

    #For buying/selling
    elif user_input[0:5]=="-open":
        ticker_range_string = user_input[6::]
        ticker_string = ticker_range_string.partition(" ")[0]
        ticker = YahooFin.Ticker(ticker_string)
        amount = ticker_range_string.partition(" ")[2]
        positions.append(Position(ticker_string,amount,ticker.info['regularMarketPrice']))
        main()

    elif user_input=="-exit":
        write_data(positions)
        quit()

#Get info list for a certain product
def general_stock_info(ticker):
    for key,value in ticker.info.items():
        print(key, ":", value)
    main()


#Display graph of price over time
def price_graph(ticker, time,ticker_string):
    gr = ticker.history(time)
    print(gr)
    gr.plot(kind='line', y='Close')
    plt.title(ticker_string)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()
    main()


# Using CSV file to store transactions at the end
def write_data(positions):
    with open(file,"a", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in positions:
            csvwriter.writerow([i.product,i.amount,i.purchase_price])


main()
