from fastapi import FastAPI
import psycopg2
from config import config
from models.Signup import Signup



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

    result = cursor.fetchall()

    if len(result)!=1:
        return {"message":"login failed"}
    
    else:

        return {"message": "logged in successfully"}