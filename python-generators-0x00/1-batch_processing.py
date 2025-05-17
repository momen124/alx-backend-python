import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows
    except Error as e:
        print(f"Error streaming batches: {e}")
    finally:
        cursor.close()
        connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user