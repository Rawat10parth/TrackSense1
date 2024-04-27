# Import necessary libraries
import time
from urllib import request

import timers
from pynput import keyboard, mouse
import threading
from threading import Thread
import pygetwindow as gw
from flask import Flask, render_template
from database import get_window_time, update_or_insert_window_time
from plyer import notification
import psutil

app = Flask(__name__)


class ScreenTimeTracker:

    def __init__(self):
        # Initialize variables
        self.start_time = time.time()
        self.total_time = 0
        self.idle_time = 5 * 60  # 5 minutes
        self.activity_detected = False  # Flag to track any activity
        self.last_application_start_time = None
        self.last_application = None
        self.app_limits = {}
        self.timers = {}

        self.set_application_limit("PyCharm", 60)

        # Start the idle checker in a separate thread
        idle_checker = threading.Thread(target=self.check_idle)
        idle_checker.start()

        # Function to start a timer for a given application
    def start_timer(self, application_name, duration):
        time.sleep(duration)
        # Code to handle timer completion, e.g., terminate application or trigger notification
        print(f"Timer for {application_name} completed!")

    # Route to render the alarm.html template
    @app.route('/index', methods=['GET', 'POST'])
    def set_timer(self):
        if request.method == 'POST':
            application_name = request.form['application']
            duration = int(request.form['duration'])
            # Start a new timer in a separate thread
            timer_thread = Thread(target=self.start_timer, args=(application_name, duration))
            timer_thread.start()
            # Store the timer in the dictionary
            self.timers[application_name] = timer_thread
            return "Timer set successfully!"
        else:
            return render_template('alarm.html')

    # Define activity event
    def on_activity(self):
        self.activity_detected = True
        self.start_time = time.time()

    # Define the idle check function
    def check_idle(self):
        current_application = None
        window_start_time = None

        while True:
            # Check for inactivity
            if not self.activity_detected:
                idle_time_increment = time.time() - self.start_time  # Calculate the idle time increment
                self.total_time += idle_time_increment  # Add the idle time increment to the total time

            # Reset the start time regardless of activity
            self.start_time = time.time()

            # Reset activity flag
            self.activity_detected = False

            # Capture active window title
            active_window = gw.getActiveWindow()
            window_title = active_window.title if active_window else ""

            application_name = self.extract_application_name(window_title)

            # If the active window changes
            if application_name != self.last_application:
                print(f"Application : {application_name}")
                if self.last_application in self.app_limits:
                    limit, usage = self.app_limits[self.last_application]
                    if self.last_application_start_time is not None:
                        application_elapsed_time = time.time() - self.last_application_start_time
                        usage += application_elapsed_time

                    if usage >= limit:
                        notification.notify(
                            title="Application Limit Exceeded",
                            message=f"The usage limit for {self.last_application} has been reached.",
                            timeout=10
                        )
                        time.sleep(15)

                    self.app_limits[self.last_application] = (limit, usage)

                # Calculate time spent on previous window and add to total_time
                if self.last_application_start_time is not None:
                    application_elapsed_time = time.time() - self.last_application_start_time
                    self.total_time += application_elapsed_time
                    hours, rem = divmod(application_elapsed_time, 3600)
                    minutes, seconds = divmod(rem, 60)
                    print(f"Time spent on '{self.last_application}': {int(hours)}:{int(minutes)}:{int(seconds)}")
                    update_or_insert_window_time(self.last_application, application_elapsed_time)

                # Update current window and start time
                self.last_application = application_name
                self.last_application_start_time = time.time()

            # Sleep for idle check interval
            time.sleep(1)  # Check for idle time every second

    def is_limit_exceeded(self, application_name, limit):
        if application_name in self.app_limits:
            app_limit, app_usage = self.app_limits[application_name]
            return app_usage >= limit
        return False

    def terminate_application(self, application_name):
        try:
            for proc in psutil.process_iter():
                if application_name.lower() in proc.name().lower():
                    proc.kill()
                    print(f"{application_name} has been terminated")
                    break
        except Exception as e:
            print(f"Error while terminating {application_name}: {e}")

    def extract_application_name(self, window_title):
        if "|" in window_title:
            app_name = window_title.split("|")[1].strip()
            if not app_name.endswith('.py'):
                return app_name
            else:
                return "PyCharm"
        elif "-" in window_title:
            app_name = window_title.split("-")[1].strip()
            if not app_name.endswith('.py'):
                return app_name
            else:
                return "PyCharm"
        else:
            app_name = window_title.strip()
            if not app_name.endswith('.py'):
                return app_name
            else:
                return "PyCharm"
        return None

    def start_tracking(self):
        # Start listeners for keyboard and mouse events
        with keyboard.Listener(on_press=lambda _: self.on_activity(),
                               on_release=lambda _: self.on_activity()) as k_listener, \
                mouse.Listener(on_move=lambda x, y: self.on_activity(),
                               on_click=lambda x, y, button, pressed: self.on_activity()) as m_listener:
            k_listener.join()
            m_listener.join()

    def get_last_window_title(self):
        return self.last_application

    def set_last_window_title(self, application_name):
        self.last_application = application_name

    def set_application_limit(self, application_name, limit):
        self.app_limits[application_name] = (limit, 0)


@app.route('/')
def index():
    return "TrackSense"


if __name__ == "__main__":
    tracker = ScreenTimeTracker()
    tracker.start_tracking()
    app.run(debug=True)