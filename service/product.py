

import datetime
import yfinance as yf
from service.login import login_service
from models.Signup import Signup


def buy_service(cursor,conn,product):

    login_data = Signup(username = product.username,password = product.password)
    response = login_service(cursor,login_data)


    if response["message"] == "logged in successfully":

        #Get price of product and payment amount
        UserId = response["UserId"]
        timestamp = datetime.datetime.now()
        ticker = yf.Ticker(product.name)
        last_price = ticker.fast_info["lastPrice"]
        payment = last_price*product.amount

        #Check if user has enough cash
        cursor.execute("SELECT Amount FROM Positions WHERE UserId = '%s' AND Product = 'cash'" % (UserId))
        current_amount = cursor.fetchall()[0][0]

        if current_amount>= payment:
            cursor.execute("UPDATE Positions SET Amount = Positions.Amount - '%s' WHERE UserId = '%s' AND Product = 'cash'"%(payment,UserId))
            cursor.execute("INSERT INTO Positions (UserId,Amount,Product) VALUES ('%s','%s','%s') ON CONFLICT (UserId,Product) DO UPDATE SET Amount = Positions.Amount + '%s' " % (UserId,product.amount,product.name, product.amount))
            cursor.execute("INSERT INTO TransactionHistory (UserID,Product,Amount,Price,Timestamp) VALUES ('%s','%s','%s','%s','%s')" % (UserId,product.name,product.amount,last_price,timestamp))
            conn.commit()

            return {"message":"Sucessfully executed buy"}

        else:
            return {"message":"Insufficient funds"}
        
        

    else:
        return {"message": "unable to buy"}
    
def sell_service(cursor,conn,product):

    login_data = Signup(username = product.username,password = product.password)
    response = login_service(cursor,login_data)


    if response["message"] == "logged in successfully":

        #Get price of product and payment amount
        UserId = response["UserId"]
        timestamp = datetime.datetime.now()
        ticker = yf.Ticker(product.name)
        last_price = ticker.fast_info["lastPrice"]
        payment_received = last_price*product.amount

        #Check if user has enough units of the product
        cursor.execute("SELECT Amount FROM Positions WHERE UserId = '%s' AND Product = '%s'" % (UserId,product.name))
        current_amount = cursor.fetchall()[0][0]

        if current_amount>= product.amount:
            cursor.execute("UPDATE Positions SET Amount = Positions.Amount + '%s' WHERE UserId = '%s' AND Product = 'cash'"%(payment_received,UserId)) #Increase cash by amount received
            cursor.execute("UPDATE Positions SET Amount = Positions.amount - '%s' WHERE Product = '%s'"% (product.amount,product.name)) #Reduce amount of product held
            cursor.execute("INSERT INTO TransactionHistory (UserID,Product,Amount,Price,Timestamp) VALUES ('%s','%s','%s','%s','%s')" % (UserId,product.name,-product.amount,last_price,timestamp)) #Insert record in history with negative amount to indicate sell
            conn.commit()

            return {"message":"Sucessfully executed sell"}

        else:
            return {"message":"Not enough units in account"}
        
        

    else:
        return {"message": "unable to sell"}