

def login_service(cursor,login):
    cursor.execute("SELECT * FROM Users WHERE Username = '%s' AND Password = '%s'" % (login.username,login.password))

    result = cursor.fetchall()

    if len(result)!=1:
        return {"message":"login failed"}
    
    
    else:
        #Set the userId so that it can be used in future queries
        UserId = result[0][0]
        return {"message": "logged in successfully","UserId": UserId}

def signup_service(cursor,conn,signup):
    cursor.execute("SELECT * FROM Users WHERE Username  = '%s'" % (signup.username))
    result = cursor.fetchall()

    if len(result)!=0:

        return {"message":"username %s is not available"%(signup.username)}
    
    else:

        cursor.execute(("INSERT INTO Users (Username,Password) VALUES ('%s','%s')"%(signup.username,signup.password)))
        conn.commit()

        return {"message":"Sucessfully signed up"}