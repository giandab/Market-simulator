

from collections import Counter
import datetime
import pandas as pd
import yfinance as yf
from service.login import login_service
from models.Signup import Signup


def history_service(cursor,auth):

    login_data = Signup(username = auth.username,password = auth.password)
    response = login_service(cursor,login_data)

    if response["message"] == "logged in successfully":
        UserId = response["UserId"]
        cursor.execute("SELECT * FROM TransactionHistory WHERE UserId = '%s'"%(UserId))
        history = cursor.fetchall()

        return {"message":history}

    else:
        return {"message":"unable to retrieve history"}
    
def positions_service(cursor,auth):
    login_data = Signup(username = auth.username,password = auth.password)
    response = login_service(cursor,login_data)

    if response["message"] == "logged in successfully":
        UserId = response["UserId"]
        cursor.execute("SELECT * FROM Positions WHERE UserId = '%s'"%(UserId))
        positions = cursor.fetchall()

        return {"message":positions}

    else:
        return {"message":"unable to retrieve positions"}

def balance__over_time_service(cursor,auth):
    
    login_data = Signup(username = auth.username,password = auth.password)
    response = login_service(cursor,login_data)

    if response["message"] == "logged in successfully":
        UserId = response["UserId"]
        cursor.execute("SELECT * FROM TransactionHistory WHERE UserId = '%s'"%(UserId))
        history = cursor.fetchall()

        if len(history) ==0:
            return {"message","No Balance history to show yet"}
        else:

            # This block creates a dictionary with the DB retrieved dates as keys and values as dictionaries in form {product: amount}. It needs cleaning up and optimising.
            history.sort(key=lambda x:x[4])
            dates_dict = {}
            product_hist_to_retrieve = []
            for record in history:
                dates_dict[record[4].date()] = {}
            for record in history:
                dates_dict[record[4].date()][record[1]] = 0
                if record[1] not in product_hist_to_retrieve:
                    product_hist_to_retrieve.append(record[1])
            product_hist_to_retrieve.remove("cash")
            for record in history:
                dates_dict[record[4].date()][record[1]] = dates_dict[record[4].date()][record[1]] + record[2]

            #This gets the list dates not on the list - from the earliest date on the db to now. It adds them to the dates_dict created above - "filling in the gaps"
            addtional_dates = pd.date_range(start=min(list(dates_dict.keys())),end=datetime.datetime.now().date())
            addtional_dates = addtional_dates.to_pydatetime()
            for date in addtional_dates:
                date = date.date()
                if date not in list(dates_dict.keys()):
                    dates_dict[date] = {}
                else:
                    pass

            
            #sort dates as the next step will not work if the dates are not in order
            keys = list(dates_dict.keys())
            keys.sort()
            dates_dict = {i: dates_dict[i] for i in keys}
            
            #Iteratively add the previous date's positions to the next to get the total positions held on each date
            dates = list(dates_dict.keys())
            for i in range(1,len(dates)):
                dates_dict[dates[i]] = dict(Counter(dates_dict[dates[i]])+Counter(dates_dict[dates[i-1]]))

            #Get prices for each product in list from start to now
            tickers = {}
            for product in product_hist_to_retrieve:
                tickers[product] = yf.Ticker(product).history(start = list(dates_dict.keys())[0],end= list(dates_dict.keys())[-1])
                tickers[product].index = pd.to_datetime(tickers[product].index).date
                tickers[product].index = tickers[product].index.astype(str)

            #Calculate value of total products held on each day
            values = {}
            for date in list(dates_dict.keys()):
                values[date] = calculate_values(date,dates_dict,tickers)

            return {"message":values}

    else:
        return {"message":"unable to retrieve history"}
    
def calculate_values(date,dates_dict,tickers):
    "helper function for balanceOverTime endpoint"

    value = 0
    for product in list(dates_dict[date].keys()):
        try:
            if product == 'cash':
                value += dates_dict[date]['cash']

            else:
                value += getLastAvailableValue(date,tickers,product,dates_dict)

        except KeyError as e:
            #If a product is bought on a weekend (i.e. the first day is missing in the 'close' data)
            #Then the above solution will cause an error as there is no index -1 in values
            #This is a temp 'fix'
            value = 0
    
    return value

def getLastAvailableValue(date,tickers,product,dates_dict):
    if date in dates_dict.keys():
        try:
           return tickers[product].at[str(date),'Close']
        except:
           return getLastAvailableValue(date+datetime.timedelta(days=-1),tickers,product,dates_dict)
    else:
        return 0