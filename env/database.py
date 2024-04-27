import pyodbc
import mysql.connector

# cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
#                       'Server=tcp:minortrack.database.windows.net,1433;'
#                       'Database=tracksense;'
#                       'Uid=parth;'
#                       'Pwd=Rawat@10;'
#                       'Encrypt=yes;'
#                       'TrustServerCertificate=no;'
#                       'Connection Timeout=30;')
cnxn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="tracksense",
            )


def get_window_time(window_title):
    try:
        # Retrieve the total time spent on a window from the database
        cursor = cnxn.cursor()
        cursor.execute("SELECT total_time FROM window_time WHERE window_title=%s", (window_title,))
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()


def update_or_insert_window_time(window_title, time_spent):
    try:
        # Create a cursor using the connection
        cursor = cnxn.cursor()

        # Execute the SQL query
        cursor.execute("SELECT total_time FROM window_time WHERE window_title=%s", (window_title,))
        result = cursor.fetchone()

        if result:
            # Update existing record
            total_time = float(result[0]) + time_spent
            cursor.execute("UPDATE window_time SET total_time=%s WHERE window_title=%s", (total_time, window_title))
        else:
            # Insert new record
            cursor.execute("INSERT INTO window_time (window_title, total_time) VALUES (%s, %s)", (window_title, time_spent))

        # Commit the transaction
        cnxn.commit()
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
    finally:
        # Close cursor
        if 'cursor' in locals() and cursor is not None:
            cursor.close()