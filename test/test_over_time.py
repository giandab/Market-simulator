from fastapi.testclient import TestClient
from models.Signup import Signup
from main import app
import psycopg2
from config import config
from test_deposit_withdraw import test_signup,test_deposit
from test_deposit_withdraw import test_signup
from testData.populate_transactions import testdata

#database connection
params = config()
conn = psycopg2.connect(**params)

cursor = conn.cursor()

user1 = Signup(username="username1",password="password1")
client = TestClient(app)

    

def test_populate_transactions_history_db():

    test_signup
    cursor.execute("SELECT UserId FROM Users WHERE Username = 'username1'")
    userId = cursor.fetchone()[0]

    for transaction in testdata:
        cursor.execute("INSERT INTO TransactionHistory (Product, Amount ,Price ,Timestamp,UserId) VALUES ('%s','%s','%s','%s','%s')" % (transaction["product"],transaction["amount"],transaction["price"],transaction["timestamp"],userId))
    conn.commit()
    
    response = client.post("/getBalanceOverTime",json={"username":user1.username,"password":user1.password})

    print(response.json()["message"])

def test_cleanup():
    #Cleanup - delete records and close connection
    cursor.execute("DELETE FROM Users WHERE Username = '%s'"%(user1.username))

    conn.commit()
    conn.close()

