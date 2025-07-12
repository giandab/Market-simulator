from fastapi.testclient import TestClient
from models.Signup import Signup
from main import app
import psycopg2
from config import config

#database connection
params = config()
conn = psycopg2.connect(**params)

cursor = conn.cursor()

user1 = Signup(username="username1",password="password1")
client = TestClient(app)


def test_signup():

    response = client.post("/signup",json = {"username":user1.username,"password":user1.password})

    assert response.json() == {"message":"Sucessfully signed up"}



#Cleanup - delete records and close connection
cursor.execute("DELETE FROM Users WHERE Username = '%s'"%(user1.username))

conn.commit()
conn.close()