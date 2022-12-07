import mysql.connector

# NOTE THAT XAMP AND MYSQL CLI HAS DIFFERENT SET UP 
mydb = mysql.connector.connect(host = "localhost",user = "root",passwd = "")

# SET database cursor
my_cursor = mydb.cursor()

#Code line for creating a new database in MYSQL
my_cursor.execute("CREATE DATABASE FCC_FLASKDB")

# QUERYING MYSQL to show databases
my_cursor.execute("SHOW DATABASES")

# PRINTING the queried result from database
for i in my_cursor:
    print(i)