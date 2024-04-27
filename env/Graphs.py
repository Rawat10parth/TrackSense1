import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Replace with your MySQL database connection details
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "tracksense"
}

# Connect to the MySQL database
conn = mysql.connector.connect(**db_config)

# Define a query to retrieve data from the database
query = """
SELECT window_title, total_time
FROM window_time
"""  # Replace 'your_table' with the name of your table

# Execute the query and read the data into a pandas DataFrame
df = pd.read_sql(query, conn)

# Close the database connection
conn.close()

# Plot the data
plt.figure(figsize=(10, 6))
plt.bar(df['window_title'], df['total_time'], color='blue')
plt.xlabel('Window_title')
plt.ylabel('Total_Time')
plt.title('Time by Window')

# Show the bar graph
plt.show()
