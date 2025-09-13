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
        timestamp = datetime.datetime.now()

        #Inserts new record for cash amount or updates if there is an existing one
        cursor.execute("INSERT INTO Positions (UserId,Amount,Product) VALUES ('%s','%s','%s') ON CONFLICT (UserId,Product) DO UPDATE SET Amount = Positions.Amount + '%s' " % (UserId,amount.amount,"cash", amount.amount))
        cursor.execute("INSERT INTO TransactionHistory (UserID,Product,Amount,Price,Timestamp) VALUES ('%s','%s','%s','%s','%s')" % (UserId,"cash",amount.amount,1,timestamp))
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
        timestamp = datetime.datetime.now()

        cursor.execute("SELECT Amount FROM Positions WHERE UserId = '%s' AND Product = 'cash'" % (UserId))

        current_amount = cursor.fetchall()[0][0]

        if current_amount >= amount.amount:

            cursor.execute("UPDATE Positions SET Amount = Positions.Amount - '%s' WHERE UserId = '%s' AND Product = 'cash'"%(amount.amount,UserId))
            cursor.execute("INSERT INTO TransactionHistory (UserID,Product,Amount,Price,Timestamp) VALUES ('%s','%s','%s','%s','%s')" % (UserId,"cash",-amount.amount,1,timestamp))
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


@app.post("/sell")
def sellProduct(product:Product):

    login_data = Signup(username = product.username,password = product.password)
    response = login(login_data)


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
    
@app.post("/getHistory")
def getHistory(auth:Signup):

    login_data = Signup(username = auth.username,password = auth.password)
    response = login(login_data)

    if response["message"] == "logged in successfully":
        UserId = response["UserId"]
        cursor.execute("SELECT * FROM TransactionHistory WHERE UserId = '%s'"%(UserId))
        history = cursor.fetchall()

        return {"message":history}

    else:
        return {"message":"unable to retrieve history"}
    
@app.post("/getPositions")
def getHistory(auth:Signup):

    login_data = Signup(username = auth.username,password = auth.password)
    response = login(login_data)

    if response["message"] == "logged in successfully":
        UserId = response["UserId"]
        cursor.execute("SELECT * FROM Positions WHERE UserId = '%s'"%(UserId))
        positions = cursor.fetchall()

        return {"message":positions}

    else:
        return {"message":"unable to retrieve positions"}
    
@app.post("/getBalanceOverTime")
def getBalanceOverTime(auth:Signup):

    login_data = Signup(username = auth.username,password = auth.password)
    response = login(login_data)

    if response["message"] == "logged in successfully":
        UserId = response["UserId"]
        cursor.execute("SELECT * FROM TransactionHistory WHERE UserId = '%s'"%(UserId))
        history = cursor.fetchall()

        print("DEBUG History" ,history)

        #1. we sort every transaction by date
        #2. we get a list of all unique dates that have transactions
        #3. on the first date we add together all the products 
        #4. on each subsequent date we also add up products and carry over those from the previous date
        #5. we should end up with a list of dates with products owned on that date
        #6. we extend the list to cover dates without transactions so we have a full list until today.
        #7. we now want to find the price of each product on each day :  data = yf.Ticker("ABEV3.SA") , data = data.history(start="2010-01-01",  end=now)

        return {"message":history}

    else:
        return {"message":"unable to retrieve history"}