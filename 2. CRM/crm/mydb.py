import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS crm_shubham")

mycursor.close()

print("Database created successfully")