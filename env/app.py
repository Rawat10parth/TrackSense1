import bcrypt
from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                      'Server=tcp:minortrack.database.windows.net,1433;'
                      'Database=tracksense;'
                      'Tables=users;'
                      'Uid=parth;'
                      'Pwd=Rawat@10;'
                      'Encrypt=yes;'
                      'TrustServerCertificate=no;'
                      'Connection Timeout=30;')


@app.route('/')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_submit():
    if request.method == 'POST':
        try:
            first_name = request.form.get('first-name')
            last_name = request.form.get('last-name')
            email = request.form.get('email')
            password = request.form.get('password')

            # Hash the password before storing it in the database
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            cursor = cnxn.cursor()
            cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (?,?,?,?)",
                           (first_name, last_name, email, hashed_password))
            cnxn.commit()
            cursor.close()

            return redirect(url_for('signup_success'))
        except pyodbc.Error as err:
            return f"An error occurred: {err}", 500
        except Exception as e:
            return f"An error occurred: {e}", 500


@app.route('/signup-success')
def signup_success():
    return "Signup successful"


if __name__ == '__main__':
    app.run(debug=True)