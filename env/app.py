import signup
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Adjust database connection parameters according to your MySQL setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="user"
)


@app.route('/')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_submit():
    if request.method == 'POST':
        try:
            first_name = request.form.get('first-name')  # Adjust form field names
            last_name = request.form.get('last-name')  # Adjust form field names
            email = request.form.get('email')  # Adjust form field names
            password = request.form.get('password')  # Adjust form field names

            cursor = db.cursor()
            # Adjust table name and column names in the SQL query
            cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                           (first_name, last_name, email, password))
            db.commit()  # Commit the transaction
            cursor.close()

            return "Signup successful"
        except Exception as e:
            return f"An error occurred: {e}", 500


if __name__ == '__main__':
    app.run(debug=True)