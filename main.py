from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel
from config import config


class Signup(BaseModel):
    username: str
    password: str

#database connection
params = config()
conn = psycopg2.connect(**params)

cursor = conn.cursor

# Create a FastAPI application
app = FastAPI()

# Define a route at the root web address ("/")
@app.post("/signup")
def signup(signup:Signup):
    statement = "INSERT INTO Users (Username,Password) VALUES ({signup.username},{signup.password})"

@app.post("/login")
def login(signup:Signup):
    statement = "SELECT * FROM Users WHERE Username = {signup.username} AND Password = {signup.password}"