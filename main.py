import yfinance as YahooFin

def main():
    user_input=input("Type '-info [ticker]' to get general information")
    if user_input[0:5]=="-info":
        get_ticker_info = YahooFin.Ticker(user_input[6:])
        general_stock_info(get_ticker_info)
    if user_input=="exit":
        quit()

def general_stock_info(ticker):
    for key,value in ticker.info.items():
        print(key, ":", value)
    main()

main()
