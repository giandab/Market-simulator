#Used to set up tables if they aren't already created

import psycopg2
from config import config

#database connection
params = config()
conn = psycopg2.connect(**params)

cursor = conn.cursor()

create_users = "CREATE TABLE IF NOT EXISTS Users (UserId SERIAL PRIMARY KEY, Username varchar(255), Password varchar(255));"
create_positions = "CREATE TABLE IF NOT EXISTS Positions (PositionId SERIAL PRIMARY KEY, Amount real, Product varchar(255), UserId int, CONSTRAINT fk_user FOREIGN KEY (UserId) REFERENCES Users(UserId) ON DELETE CASCADE,CONSTRAINT unique_id_prod UNIQUE (UserId,Product));"
create_history = "CREATE TABLE IF NOT EXISTS TransactionHistory (TransactionID SERIAL PRIMARY KEY, Product varchar(255), Amount real, Price real, Date date, UserId int, CONSTRAINT fk_user FOREIGN KEY (UserId) REFERENCES Users(UserId) ON DELETE CASCADE);"


cursor.execute(create_users)
cursor.execute(create_positions)
cursor.execute(create_history)

conn.commit()
print("Tables created successfully")
conn.close()