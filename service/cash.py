

import datetime

from models.Signup import Signup
from service.login import login_service


def deposit_service(cursor,conn,amount):
    login_data = Signup(username = amount.username,password = amount.password)
    response = login_service(cursor,login_data)

    if response["message"] == "logged in successfully":

        UserId = response["UserId"]
        timestamp = datetime.datetime.now()

        #Inserts new record for cash amount or updates if there is an existing one
        cursor.execute("INSERT INTO Positions (UserId,Amount,Product) VALUES ('%s','%s','%s') ON CONFLICT (UserId,Product) DO UPDATE SET Amount = Positions.Amount + '%s' " % (UserId,amount.amount,"cash", amount.amount))
        cursor.execute("INSERT INTO TransactionHistory (UserID,Product,Amount,Price,Timestamp) VALUES ('%s','%s','%s','%s','%s')" % (UserId,"cash",amount.amount,1,timestamp))
        conn.commit()

        return {"message":"successfully deposited cash"}
    
    else:
        return {"message": "unable to deposit"}
    
def withdraw_service(cursor,conn,amount):
    login_data = Signup(username = amount.username,password = amount.password)
    response = login_service(cursor,login_data)

    if response["message"] == "logged in successfully":

        UserId = response["UserId"]
        timestamp = datetime.datetime.now()

        cursor.execute("SELECT Amount FROM Positions WHERE UserId = '%s' AND Product = 'cash'" % (UserId))

        current_amount = cursor.fetchall()[0][0]

        if current_amount >= amount.amount:

            cursor.execute("UPDATE Positions SET Amount = Positions.Amount - '%s' WHERE UserId = '%s' AND Product = 'cash'"%(amount.amount,UserId))
            cursor.execute("INSERT INTO TransactionHistory (UserID,Product,Amount,Price,Timestamp) VALUES ('%s','%s','%s','%s','%s')" % (UserId,"cash",-amount.amount,1,timestamp))
            conn.commit()

            return {"message": "successfully withdrew cash"}

        else:

            return {"message":"insufficient funds"}
    
    else:
        return {"message": "unable to withdraw"}