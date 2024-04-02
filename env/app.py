from flask import Flask, request, render_template, redirect, session
import pyodbc

app = Flask(__name__)

cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                      'Server=tcp:minortrack.database.windows.net,1433;'
                      'Database=tracksense;'
                      'Table=users;'
                      'Uid=parth;'
                      'Pwd=Rawat@10;'
                      'Encrypt=yes;'
                      'TrustServerCertificate=no;'
                      'Connection Timeout=30;')

app.secret_key = 'secret-key'


@app.route('/')
def index():
    return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        cursor = cnxn.cursor()
        cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (?,?,?,?)",
                       (first_name, last_name, email, password))
        cnxn.commit()
        cursor.close()
        return redirect('/login')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = cnxn.cursor()

        cursor.execute("SELECT email, password FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Check if the password matches
            if password == user.password:
                # Store the user's email in the session
                session['email'] = user.email
                return redirect('/dashboard')
            else:
                # Password incorrect
                return render_template('login.html', error='Invalid password')
        else:
            # User not found
            return render_template('login.html', error='User not found')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        cursor = cnxn.cursor()
        cursor.execute("SELECT first_name FROM users WHERE email=?", (session['email'],))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('dashboard.html', user=user)

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
