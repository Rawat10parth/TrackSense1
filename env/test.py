import time
import threading
import pygetwindow as gw
from pynput import keyboard, mouse


class ScreenTimeTracker:
    def __init__(self):
        self.start_time = time.time()
        self.total_time = 0
        self.idle_time = 5 * 60  # 5 minutes
        self.activity_detected = False  # Flag to track any activity

        # Start the idle checker in a separate thread
        idle_checker = threading.Thread(target=self.check_idle)
        idle_checker.start()

    def on_activity(self):
        self.activity_detected = True
        self.start_time = time.time()

    def check_idle(self):
        while True:
            # Check for inactivity
            if not self.activity_detected:
                # Increment idle time
                self.total_time += self.idle_time
            # Reset activity flag
            self.activity_detected = False

            # Capture active window title
            active_window = gw.getActiveWindow()
            window_title = active_window.title if active_window else ""
            print(f"Active window title: {window_title}")

            # Sleep for idle check interval
            time.sleep(1)  # Check for idle time every minute

    def start_tracking(self):
        # Start listeners for keyboard and mouse events
        with keyboard.Listener(on_press=lambda _: self.on_activity(),
                               on_release=lambda _: self.on_activity()) as k_listener, \
                mouse.Listener(on_move=lambda x, y: self.on_activity(),
                               on_click=lambda x, y, button, pressed: self.on_activity()) as m_listener:
            k_listener.join()
            m_listener.join()


if __name__ == "__main__":
    tracker = ScreenTimeTracker()
    tracker.start_tracking()
