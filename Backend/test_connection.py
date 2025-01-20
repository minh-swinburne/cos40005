import mysql.connector

def test_connection():
    connection = None  # Initialize connection outside try block
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Admin123@",
            database="health"
        )
        if connection.is_connected():
            print("Database connection successful!")
    except Exception as e:
        print("Error connecting to database:", e)
    finally:
        if connection and connection.is_connected():  # Check if connection is not None
            connection.close()
            print("Database connection closed.")

test_connection()

