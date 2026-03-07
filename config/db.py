import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG ={
    "host":os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password":os.getenv("DB_PASSWORD"),
    "database":os.getenv("DB_NAME")
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