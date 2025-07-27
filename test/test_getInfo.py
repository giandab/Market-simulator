from fastapi.testclient import TestClient
from models.Signup import Signup
from main import app
import psycopg2
from config import config
from test_deposit_withdraw import test_signup,test_deposit


#Tests the initial flow of the service
#A user that has signed up and logged in
#Can successfully withdraw and deposit cash

#database connection
params = config()
conn = psycopg2.connect(**params)

cursor = conn.cursor()

user1 = Signup(username="username1",password="password1")
client = TestClient(app)

def test_setup():
    test_signup
    test_deposit

def test_buy():

    response = client.post("/buy",json = {"username":user1.username,"password":user1.password,"name":"AAPL","amount":1})
    assert response.json()["message"] == "Sucessfully executed buy"


def test_History():
    response = client.post("/getHistory",json = {"username":user1.username,"password":user1.password})
    response = response.json()["message"]
    print("DEBUG TransactionHistory",response)

    assert response != "unable to retrieve history"

def test_Positions():

    response = client.post("/getPositions",json = {"username":user1.username,"password":user1.password})
    response = response.json()["message"]
    print("DEBUG Positions",response)

    assert response != "unable to retrieve positions"

def test_cleanup():
    #Cleanup - delete records and close connection
    cursor.execute("DELETE FROM Users WHERE Username = '%s'"%(user1.username))

    conn.commit()
    conn.close()
