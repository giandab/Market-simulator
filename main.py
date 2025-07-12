from fastapi import FastAPI
import psycopg2
from config import config
from models.Signup import Signup



#database connection
params = config()
conn = psycopg2.connect(**params)

cursor = conn.cursor

# Create a FastAPI application
app = FastAPI()

# Define a route at the root web address ("/")
@app.post("/signup")
def signup(signup:Signup):

    check_username = "SELECT * FROM Users WHERE Username  = {signup.username}"
    cursor.execute(check_username)
    result = cursor.fetchall()

    if len(result)!=0:

        return {"message":"username {signup.username} is not available"}
    
    else:

        statement = "INSERT INTO Users (Username,Password) VALUES ({signup.username},{signup.password})"

        cursor.execute(statement)
        conn.commit()

        return {"message":"Sucessfully signed up"}

@app.post("/login")
def login(login:Signup):

    statement = "SELECT * FROM Users WHERE Username = {login.username} AND Password = {login.password}"

    cursor.execute(statement)

    result = cursor.fetchall()

    if len(result)!=1:
        return {"message":"login failed"}
    
    else:

        return {"message": "logged in successfully"}