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
    prod_amount = helper_check_amount_in_db("AAPL")

    assert response.json()["message"] == "Sucessfully executed buy"
    assert prod_amount == 1

def test_buy_excessive():

    response = client.post("/buy",json = {"username":user1.username,"password":user1.password,"name":"AAPL","amount":100})
    assert response.json()["message"] == "Insufficient funds"

def test_sell():
    response = client.post("/sell",json = {"username":user1.username,"password":user1.password,"name":"AAPL","amount":1})

    product_amount = helper_check_amount_in_db("AAPL")
    assert response.json()["message"] == "Sucessfully executed sell"
    assert product_amount == 0.0

def test_sell_excessive():

    response = client.post("/sell",json = {"username":user1.username,"password":user1.password,"name":"AAPL","amount":100})
    assert response.json()["message"] == "Not enough units in account"

def test_cleanup():
    #Cleanup - delete records and close connection
    cursor.execute("DELETE FROM Users WHERE Username = '%s'"%(user1.username))

    conn.commit()
    conn.close()


def helper_check_amount_in_db(productName):
    #Checking amount of product in DB
    response_login = client.post("/login",json = {"username":user1.username,"password":user1.password})
    cursor.execute("SELECT Amount FROM Positions WHERE UserId = '%s' AND Product = '%s'" % (response_login.json()["UserId"],productName))
    product_amount = cursor.fetchall()[0][0]
    return product_amount