from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
import time
from pygetwindow import getActiveWindow
import threading
from flask import jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from plyer import notification
import threading
import pygame

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection setup
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "tracksense"
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        emaill = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (emaill, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['user_id'] = user[0]  # Assuming 'user[0]' is the user_id in your users table
            session['user_email'] = user[1]  # Assuming 'user[1]' is the email column in your users table
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)',
                       (first_name, last_name, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT app_name, SUM(duration) as total_duration FROM app_usage GROUP BY app_name')
    app_times = cursor.fetchall()
    cursor.close()
    conn.close()

    app_usage_data = {app[0]: round(app[1], 2) for app in app_times}
    return render_template('dashboard.html', app_usage_data=app_usage_data)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    return redirect(url_for('login'))


def track_active_window():
    last_active_title = None
    start_time = time.time()

    while True:
        current_window = getActiveWindow()
        if current_window:
            current_title = current_window.title
            if current_title != last_active_title:
                if last_active_title is not None:
                    end_time = time.time()
                    duration = end_time - start_time
                    log_application_usage(last_active_title, duration)
                start_time = time.time()
                last_active_title = current_title
        time.sleep(1)


def log_application_usage(application_name, duration):
    # Insert email again and again add some logic
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO app_usage (app_name, duration) VALUES (%s, %s)', (application_name, duration))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/api/app-usage')
def api_app_usage():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT app_name, SUM(duration) as total_duration FROM app_usage GROUP BY app_name')
    app_times = cursor.fetchall()
    cursor.close()
    conn.close()

    app_usage_data = {app[0]: round(app[1], 2) for app in app_times}
    return jsonify(app_usage_data)


def delete_all_app_usage_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM app_usage')
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/delete-app-usage-data', methods=['POST'])
def delete_app_usage_data():
    if request.method == 'POST':
        delete_all_app_usage_data()
        return jsonify({'message': 'All data from app_usage table has been deleted.'}), 200
    else:
        return jsonify({'error': 'Method not allowed'}), 405


@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


# Route to render the set limit page

@app.route('/set-limit', methods=['GET', 'POST'])
def set_limit():
    if 'user_email' in session:
        if request.method == 'POST':
            app_name = request.form['app_name']
            time_limit = int(request.form['time_limit'])  # Convert to integer
            user_id = session['user_id']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('REPLACE INTO app_limits (user_id, app_name, time_limit) VALUES (%s, %s, %s)',
                           (user_id, app_name, time_limit))
            conn.commit()
            cursor.close()
            conn.close()
            print("Record inserted in DB for set Alarm", app_name, 'and', time_limit)
            check_time_limits(app_name)  # This might still be problematic, see below
            return redirect(url_for('dashboard'))
        return render_template('set_limit.html', user_email=session['user_email'])
    else:
        return redirect(url_for('login'))


def check_time_limits(app_name):
    limit_achieved = False
    while not limit_achieved:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Fetch the total duration from app_usage for this app
            cursor.execute('SELECT SUM(duration) FROM app_usage WHERE app_name = %s', (app_name,))
            total_duration = cursor.fetchone()[0] or 0  # Handle case where there's no duration yet
            print(f"Total duration for {app_name}: {total_duration} seconds")

            # Fetch the time limit for the app
            cursor.execute('SELECT time_limit FROM app_limits WHERE app_name = %s', (app_name,))
            limit = cursor.fetchone()
            if limit:
                if total_duration >= limit[0] * 60:  # Convert minutes to seconds
                    trigger_notification(app_name, total_duration)
                    limit_achieved = True  # Break the loop after notification
                else:
                    print(f"Current usage {total_duration} seconds is within the limit {limit[0] * 60} seconds")
            else:
                print("No limit set for this application")
                limit_achieved = True  # Break the loop if no limit is set
        finally:
            cursor.close()
            conn.close()
        time.sleep(5)  # Sleep for 5 seconds before checking again


def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def trigger_notification(app_name, duration):
    # Sending the notification
    notification.notify(
        title='Time Limit Reached',
        message=f'Limit reached for {app_name}: {duration:.2f} seconds',
        app_icon=None,
        timeout=10  # Duration in seconds the notification stays
    )

    # Play a sound
    play_sound(
        'C:/Users/Dell/Documents/college/semester6/minor 2 reports/TrackSense/env/audio.mp3')  # Ensure this path is correct

    print(f"Limit reached for {app_name}: {duration} seconds")


if __name__ == '__main__':
    threading.Thread(target=track_active_window, daemon=True).start()
    app.run(debug=True, port=8084)