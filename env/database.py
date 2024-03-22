import time
from datetime import timedelta

import mysql.connector


def get_connection():
    # Connect to MySQL database
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tracksense"
    )


def get_window_time(window_title):
    # Retrieve the total time spent on a window from the database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT total_time FROM window_times WHERE window_title=%s", (window_title,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def update_or_insert_window_time(window_title, time_spent):
    # Update or insert the time spent on a window in the database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT total_time FROM window_times WHERE window_title=%s", (window_title,))
    result = cursor.fetchone()
    if result:
        total_time = float(result[0]) + time_spent  # Convert to float
        cursor.execute("UPDATE window_times SET total_time=%s WHERE window_title=%s", (total_time, window_title))
    else:
        cursor.execute("INSERT INTO window_times (window_title, total_time) VALUES (%s, %s)", (window_title, time_spent))
    conn.commit()
    conn.close()

