from fastapi.testclient import TestClient
from models.Signup import Signup
from main import app
import psycopg2
from config import config

#Tests the initial flow of the service
#A user that has signed up and logged in
#Can successfully withdraw and deposit cash

#database connection
params = config()
conn = psycopg2.connect(**params)

cursor = conn.cursor()

user1 = Signup(username="username1",password="password1")
client = TestClient(app)


def test_signup():

    response = client.post("/signup",json = {"username":user1.username,"password":user1.password})
    assert response.json()["message"] == "Sucessfully signed up"

def test_login():

    response = client.post("/login",json = {"username":user1.username,"password":user1.password})

    assert response.json()["message"] == "logged in successfully"

def test_deposit():

    response = client.post("/deposit",json = {"amount":1000,"username":user1.username,"password":user1.password})

    assert response.json()["message"] == "successfully deposited cash"

def test_withdraw():

    response = client.post("/withdraw", json = {"amount":500,"username":user1.username,"password":user1.password})

    assert response.json()["message"] == "successfully withdrew cash"

def test_withdraw_overlimit():

    response = client.post("/withdraw", json = {"amount":5000,"username":user1.username,"password":user1.password})

    assert response.json()["message"] == "insufficient funds"

def test_cleanup():
    #Cleanup - delete records and close connection
    cursor.execute("DELETE FROM Users WHERE Username = '%s'"%(user1.username))

    conn.commit()
    conn.close()