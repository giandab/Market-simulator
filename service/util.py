
from service.login import login_service;
from models.Signup import Signup


def delete_user_service(cursor,conn,auth):

    login_data = Signup(username = auth.username,password = auth.password)
    response = login_service(cursor,login_data)

    if response["message"] == "logged in successfully":
        UserId = response["UserId"]
        cursor.execute("DELETE FROM Users WHERE UserId='%s'"%(UserId))
        conn.commit()
        return {"message":"user deleted successfully"}

    else:
        return {"message":"unable to delete user"}