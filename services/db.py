import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# load the info from env
load_dotenv()
def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def add_subscriber(email, lat, lon, threshold):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subscribers (email, lat, lon, threshold) VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO UPDATE SET lat=%s, lon=%s, threshold=%s", (email,lat, lon, threshold, lat, lon, threshold ))
    conn.commit()

def get_subscribers():
    conn = get_connection()
    cursor =  conn.cursor(cursor_factory=RealDictCursor)
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