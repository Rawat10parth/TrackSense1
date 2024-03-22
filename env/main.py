# Import necessary libraries
import time
from datetime import timedelta

from pynput import keyboard, mouse
import threading
import pygetwindow as gw
from flask import Flask
from database import get_window_time, update_or_insert_window_time

app = Flask(__name__)


class ScreenTimeTracker:

    def __init__(self):
        # Initialize variables
        self.start_time = time.time()
        self.total_time = 0
        self.idle_time = 5 * 60  # 5 minutes
        self.activity_detected = False  # Flag to track any activity
        self.last_window_title = None

        # Start the idle checker in a separate thread
        idle_checker = threading.Thread(target=self.check_idle)
        idle_checker.start()

    # Define activity event
    def on_activity(self):
        self.activity_detected = True
        self.start_time = time.time()

    # Define the idle check function
    def check_idle(self):
        current_window = None
        window_start_time = None

        while True:
            # Check for inactivity
            if not self.activity_detected:
                idle_time_increment = time.time() - self.start_time  # Calculate the idle time increment
                self.total_time += idle_time_increment  # Add the idle time increment to the total time
                print(f"Recorded {idle_time_increment} seconds of idle time.")

            # Reset the start time regardless of activity
            self.start_time = time.time()

            # Reset activity flag
            self.activity_detected = False

            # Capture active window title
            active_window = gw.getActiveWindow()
            window_title = active_window.title if active_window else ""
            print(f"Active window title: {window_title}")

            # If the active window changes
            if window_title != current_window:
                # Calculate time spent on previous window and add to total_time
                if window_start_time is not None:
                    window_elapsed_time = time.time() - window_start_time
                    self.total_time += window_elapsed_time
                    hours, rem = divmod(window_elapsed_time, 3600)
                    minutes, seconds = divmod(rem, 60)
                    print(f"Time spent on '{current_window}': {int(hours)}:{int(minutes)}:{int(seconds)}")
                    update_or_insert_window_time(current_window, window_elapsed_time)

                # Update current window and start time
                current_window = window_title
                window_start_time = time.time()

            # Sleep for idle check interval
            time.sleep(1)  # Check for idle time every second

    def start_tracking(self):
        # Start listeners for keyboard and mouse events
        with keyboard.Listener(on_press=lambda _: self.on_activity(),
                               on_release=lambda _: self.on_activity()) as k_listener, \
                mouse.Listener(on_move=lambda x, y: self.on_activity(),
                               on_click=lambda x, y, button, pressed: self.on_activity()) as m_listener:
            k_listener.join()
            m_listener.join()

    def get_last_window_title(self):
        return self.last_window_title

    def set_last_window_title(self, title):
        self.last_window_title = title


@app.route('/')
def index():
    return "TrackSense"


if __name__ == "__main__":
    tracker = ScreenTimeTracker()
    tracker.start_tracking()
    app.run(debug=True)