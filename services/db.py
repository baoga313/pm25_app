import mysql.connector
import os
from dotenv import load_dotenv
from pathlib  import Path


load_dotenv()
def get_connection():
    return mysql.connector.connect(
        host = os.getenv("MYSQL_HOST"),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        database = os.getenv("MYSQL_DATABASE"),
    )

def add_subscriber(email, lat, lon):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO subscribers (email, lat, lon) VALUES (%s, %s, %s)", (email,lat, lon))
    conn.commit()
    conn.close()
