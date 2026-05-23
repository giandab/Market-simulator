from fastapi import FastAPI
import psycopg2
from config import config
from models.Product import Product
from models.Signup import Signup
from models.CashAmount import CashAmount
import datetime
from service.cash import *
from service.history import *
from service.login import *
from service.product import *
from service.util import *
import yfinance as yf
from collections import Counter
import pandas as pd

global UserId

#database connection
params = config()
conn = psycopg2.connect(**params)

cursor = conn.cursor()

# Create a FastAPI application
app = FastAPI()


@app.post("/signup")
def signup(signup:Signup):

    return signup_service(cursor,conn, signup)

@app.post("/login")
def login(login:Signup):

    return login_service(cursor,login)

@app.post("/deposit")
def deposit_cash(amount:CashAmount):

    return deposit_service(cursor,conn,amount)
    
@app.post("/withdraw")
def withdraw_cash(amount:CashAmount):

    return withdraw_service(cursor,conn,amount)
    
@app.post("/buy")
def buyProduct(product:Product):

    return buy_service(cursor,conn,product)


@app.post("/sell")
def sellProduct(product:Product):

    return sell_service(cursor,conn,product)
    
@app.post("/getHistory")
def getHistory(auth:Signup):

    return history_service(cursor,auth)
    
@app.post("/getPositions")
def getPositions(auth:Signup):

    return positions_service(cursor,auth)
    
@app.post("/getBalanceOverTime")
def getBalanceOverTime(auth:Signup):

    return balance__over_time_service(cursor,auth)
    

@app.post("/deleteUser")
def deleteUser(auth:Signup):

    return delete_user_service(cursor,conn,auth)