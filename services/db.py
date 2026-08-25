import mysql.connector
import os
from dotenv import load_dotenv

# load the info from env
load_dotenv()
def get_connection():
    return mysql.connector.connect(
        host = os.getenv("MYSQL_HOST"),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        database = os.getenv("MYSQL_DATABASE"),
    )

def add_subscriber(email, lat, lon, threshold):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subscribers (email, lat, lon, threshold) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE lat=%s, lon=%s, threshold=%s", (email,lat, lon, threshold, lat, lon, threshold ))
    conn.commit()
    conn.close()

def get_subscribers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email, lat, lon, threshold, last_alerted FROM subscribers")
    rows = cursor.fetchall()
    conn.close()
    return rows


def mark_alerted(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE subscribers SET last_alerted = NOW() WHERE email = %s",
        (email,)
    )
    conn.commit()
    conn.close()