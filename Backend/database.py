import mysql.connector
from mysql.connector import Error

# Database connection setup
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin123@",
        database="health"
    )
