import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="Kartikey",
  password="Kartikey2011",
  database="Data"
)

print(mydb)