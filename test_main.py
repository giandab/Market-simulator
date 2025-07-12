from fastapi.testclient import TestClient
from models.Signup import Signup
from main import app

user1 = Signup(username="username1",password="password1")
client = TestClient(app)

def test_signup():

    response = client.post("/signup",json = {"username":user1.username,"password":user1.password})

    assert response.json == {"message":"Sucessfully signed up"}