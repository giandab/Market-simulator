import yfinance as YahooFin
import numpy as np
import matplotlib.pyplot as plt
import csv
import sqlite3


#Plan to replace csv with database
connection = sqlite3.connect("positions.db")
#connection.execute("""CREATE TABLE positions (ID INTEGER PRIMARY KEY AUTOINCREMENT, PRODUCT TEXT NOT NULL, QUANTITY INT NOT NULL, PURCHASE_PRICE REAL NOT NULL);""")
#connection.execute("""INSERT INTO positions (PRODUCT,QUANTITY,PURCHASE_PRICE) VALUES ('Cash',100000,1);""")
positions = {}
cursor = connection.execute("SELECT * FROM positions")
largest_key = 0
for row in cursor:
    print("row",row)
    new_dict = {row[1]:row[2],"purchase_price":row[3]}
    positions.update({row[0]:new_dict})
    largest_key+=1

#main loop
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

        if (ticker.info['regularMarketPrice'])*amount > (positions[1]["Cash"]): #if user doesn't have enough cash
            print("Insufficient cash")
            print("------------------")

        else: # Finding if the user already owns the product so record can be updated
            for i in positions:
                for x in positions[i]:
                    if x == ticker_string and ((positions[i][x] +amount) <0):
                        print("You don't own the amount of stock you are trying to sell")
                    elif x == ticker_string:
                        # Need to work out the new purchase price as the average of the previous and new - second bracketed term must be replaced
                        positions[i].update({x:(positions[i][x] +amount)})
                        connection.execute("""UPDATE positions SET QUANTITY = %s, PURCHASE_PRICE = %s WHERE PRODUCT = %s""",((positions[i][x] +amount),ticker.info['regularMarketPrice'],ticker_string))

                    else: # user doesn't own product so a new record is created
                        new_entry = {ticker_string:amount,"purchase_price":ticker.info['regularMarketPrice']}
                        positions.update({largest_key+1:new_entry})
                        largest_key+=1
                        connection.execute("""INSERT INTO positions (PRODUCT,QUANTITY,PURCHASE_PRICE) VALUES (%s,%s,%s);""",(ticker_string,amount,ticker.info['regularMarketPrice']))
        main()

    elif user_input=="-exit":
        quit()
    else:
        print("Invalid input")
        main()

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


main()
