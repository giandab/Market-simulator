from fastapi import FastAPI
import psycopg2
from config import config
from models.Signup import Signup
from models.CashAmount import CashAmount


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

    if len(result)!=0:

        return {"message":"username {signup.username} is not available"}
    
    else:

        cursor.execute(("INSERT INTO Users (Username,Password) VALUES ('%s','%s')"%(signup.username,signup.password)))
        conn.commit()

        return {"message":"Sucessfully signed up"}

@app.post("/login")
def login(login:Signup):

    cursor.execute("SELECT * FROM Users WHERE Username = '%s' AND Password = '%s'" % (login.username,login.password))

    result = cursor.fetchall()
    print(result)

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

    print(amount.__str__)

    if response["message"] == "logged in successfully":

        UserId = response["UserId"]

        #Inserts new record for cash amount or updates if there is an existing one
        cursor.execute("INSERT INTO Positions (UserId,Amount,Product) VALUES ('%s','%s','%s') ON CONFLICT (UserId,Product) DO UPDATE SET Amount = Positions.Amount + '%s' " % (UserId,amount.amount,"cash", amount.amount))
        conn.commit()

        return {"message":"successfully deposited cash"}
    
    else:
        return {"message": "unable to deposit"}
    
@app.post("/withdraw")
def withdraw_cash(amount:CashAmount):

    login_data = Signup(username = amount.username,password = amount.password)
    response = login(login_data)

    print(amount.__str__)

    if response["message"] == "logged in successfully":

        UserId = response["UserId"]

        cursor.execute("SELECT Amount FROM Positions WHERE UserId = '%s' AND Product = 'cash'" % (UserId))

        current_amount = cursor.fetchall()[0][0]

        if current_amount >= amount.amount:

            cursor.execute("UPDATE Positions SET Amount = Positions.Amount - '%s' WHERE UserId = '%s' AND Product = 'cash'"%(amount.amount,UserId))
            conn.commit()

            return {"message": "successfully withdrew cash"}

        else:

            return {"message":"insufficient funds"}
    
    else:
        return {"message": "unable to withdraw"}