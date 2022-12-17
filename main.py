import yfinance as YahooFin
import numpy as np
import matplotlib.pyplot as plt


def main():

    # Main input section
    user_input=input("Type '-info [ticker]' to get general information" + "\n" + "Type -graph [ticker] [time range] to get a price graph for times: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y and ytd." )

    # For general infromation
    if user_input[0:5]=="-info":
        get_ticker_info = YahooFin.Ticker(user_input[6:])
        general_stock_info(get_ticker_info)

    # For plotting
    elif user_input[0:6]=="-graph":
        ticker_range_string = user_input[7::] # Splitting string to detect ticker and time range
        ticker_string = ticker_range_string.partition(" ")[0]
        ticker = YahooFin.Ticker(ticker_string)
        time_range = ticker_range_string.partition(" ")[2]
        price_graph(ticker, time_range,ticker_string)

    if user_input=="exit":
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
