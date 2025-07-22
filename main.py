from fastapi import FastAPI
import psycopg2
from config import config
from models.Product import Product
from models.Signup import Signup
from models.CashAmount import CashAmount
import datetime
import yfinance as yf


global UserId

#database connection
params = config()
conn = psycopg2.connect(**params)

cursor = conn.cursor()

# Create a FastAPI application
app = FastAPI()


@app.post("/signup")
def signup(signup:Signup):

    cursor.execute("SELECT * FROM Users WHERE Username  = '%s'" % (signup.username))
    result = cursor.fetchall()
    print(result) 

    if len(result)!=0:

        return {"message":"username %s is not available"%(signup.username)}
    
    else:

        cursor.execute(("INSERT INTO Users (Username,Password) VALUES ('%s','%s')"%(signup.username,signup.password)))
        conn.commit()

        return {"message":"Sucessfully signed up"}

@app.post("/login")
def login(login:Signup):

    cursor.execute("SELECT * FROM Users WHERE Username = '%s' AND Password = '%s'" % (login.username,login.password))

    result = cursor.fetchall()

    #Set the userId so that it can be used in future queries
    UserId = result[0][0]

    if len(result)!=1:
        return {"message":"login failed"}
    
    else:

        return {"message": "logged in successfully","UserId": UserId}
    

@app.post("/deposit")
def deposit_cash(amount:CashAmount):

    login_data = Signup(username = amount.username,password = amount.password)
    response = login(login_data)

    if response["message"] == "logged in successfully":

        UserId = response["UserId"]
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        #Inserts new record for cash amount or updates if there is an existing one
        cursor.execute("INSERT INTO Positions (UserId,Amount,Product) VALUES ('%s','%s','%s') ON CONFLICT (UserId,Product) DO UPDATE SET Amount = Positions.Amount + '%s' " % (UserId,amount.amount,"cash", amount.amount))
        cursor.execute("INSERT INTO TransactionHistory (UserID,Product,Amount,Price,Date) VALUES ('%s','%s','%s','%s','%s')" % (UserId,"cash",amount.amount,1,date))
        conn.commit()

        return {"message":"successfully deposited cash"}
    
    else:
        return {"message": "unable to deposit"}
    
@app.post("/withdraw")
def withdraw_cash(amount:CashAmount):

    login_data = Signup(username = amount.username,password = amount.password)
    response = login(login_data)

    if response["message"] == "logged in successfully":

        UserId = response["UserId"]
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        cursor.execute("SELECT Amount FROM Positions WHERE UserId = '%s' AND Product = 'cash'" % (UserId))

        current_amount = cursor.fetchall()[0][0]

        if current_amount >= amount.amount:

            cursor.execute("UPDATE Positions SET Amount = Positions.Amount - '%s' WHERE UserId = '%s' AND Product = 'cash'"%(amount.amount,UserId))
            cursor.execute("INSERT INTO TransactionHistory (UserID,Product,Amount,Price,Date) VALUES ('%s','%s','%s','%s','%s')" % (UserId,"cash",-amount.amount,1,date))
            conn.commit()

            return {"message": "successfully withdrew cash"}

        else:

            return {"message":"insufficient funds"}
    
    else:
        return {"message": "unable to withdraw"}
    
@app.post("/buy")
def buyProduct(product:Product):

    login_data = Signup(username = product.username,password = product.password)
    response = login(login_data)


    if response["message"] == "logged in successfully":

        #Get price of product and payment amount
        UserId = response["UserId"]
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        ticker = yf.Ticker(product.name)
        last_price = ticker.fast_info["lastPrice"]
        payment = last_price*product.amount

        #Check if user has enough cash
        cursor.execute("SELECT Amount FROM Positions WHERE UserId = '%s' AND Product = 'cash'" % (UserId))
        current_amount = cursor.fetchall()[0][0]

        if current_amount>= payment:
            cursor.execute("UPDATE Positions SET Amount = Positions.Amount - '%s' WHERE UserId = '%s' AND Product = 'cash'"%(payment,UserId))
            cursor.execute("INSERT INTO Positions (UserId,Amount,Product) VALUES ('%s','%s','%s') ON CONFLICT (UserId,Product) DO UPDATE SET Amount = Positions.Amount + '%s' " % (UserId,product.amount,product.name, product.amount))
            cursor.execute("INSERT INTO TransactionHistory (UserID,Product,Amount,Price,Date) VALUES ('%s','%s','%s','%s','%s')" % (UserId,product.name,product.amount,last_price,date))
            conn.commit()

            return {"message":"Sucessfully executed buy"}

        else:
            return {"message":"Insufficient funds"}
        
        

    else:
        return {"message": "unable to buy"}    