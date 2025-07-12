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

    statement = "SELECT * FROM Users WHERE Username = {login.username} AND Password = {login.password}"

    cursor.execute(statement)

    result = cursor.fetchone()

    #Set the userId so that it can be used in future queries
    UserId = result[0]

    if len(result)!=1:
        return {"message":"login failed"}
    
    else:

        return {"message": "logged in successfully"}
    

@app.post("/deposit")
def deposit_cash(amount:CashAmount):

    #Inserts new record for cash amount or updates if there is an existing one
    cursor.execute("INSERT INTO Positions (UserId,Amount,Product) VALUES ('%s','%s','%s') ON CONFLICT (Product) DO UPDATE SET Amount = Amount + '%s'" % (UserId,amount.amount,"cash", amount.amount))

    return {"message":"successfully deposited cash"}