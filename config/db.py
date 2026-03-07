import mysql.connector
from mysql.connector import Error

DB_CONFIG ={
    "host":"localhost",
    "user": "Admin",
    "password":"12345",
}

def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ Connected to MySQL database successfully!")
            return connection

    except Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None
    

def close_connection(connection, cursor=None):
    if cursor:
        cursor.close()

    if connection and connection.is_connected():
        connection.close() 
        print("🔒 Connection closed.")      