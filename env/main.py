# Import necessary libraries
import time
from pynput import keyboard, mouse
import threading


class ScreenTimeTracker:

    def __init__(self):
        # Initialize variables
        self.start_time = None
        self.total_time = 0
        self.idle_time = 5 * 60  # 5 minutes
        # Start the key listener
        with (keyboard.Listener(on_press=self.on_activity, on_release=self.on_activity) as key_listener,
              mouse.Listener(on_move=self.on_activity, on_click=self.on_activity) as mouse_listener):
            # Start the idle checker in a separate thread
            idle_checker = threading.Thread(target=self.check_idle)
            idle_checker.start()

            key_listener.join()
            mouse_listener.join()

    # Define activity event
    def on_activity(self, *args):
        if self.start_time is None:
            self.start_time = time.time()
            print("Screen time tracking started.")

        else:
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            self.total_time += elapsed_time
            print(f"Recorded {elapsed_time} of screen time.")
            self.start_time = None

    # # Define the key press event
    # def on_press(self, key):
    #     if self.start_time is None:
    #         self.start_time = time.time()  # Start the timer on the first key press
    #         print("Screen time tracking started.")
    #
    # # Define the key release event
    # def on_release(self, key):
    #     if self.start_time is not None:
    #         end_time = time.time()  # End the timer when the key is released
    #         elapsed_time = end_time - self.start_time  # Calculate the elapsed time
    #         self.total_time += elapsed_time  # Add the elapsed time to the total time
    #         print(f"Recorded {elapsed_time} of screen time")
    #         hours, rem = divmod(elapsed_time, 3600)
    #         minutes, seconds = divmod(rem, 60)
    #         print(f"Recorded {int(hours)}:{int(minutes)}:{int(seconds)} of screen time.")
    #         self.start_time = None  # Reset the start

    # Define the idle check function
    def check_idle(self):
        while True:
            print("check_idle function started")
            if self.start_time is not None and time.time() - self.start_time > self.idle_time:
                elapsed_time = time.time() - self.start_time  # Calculate the elapsed time
                self.total_time += elapsed_time  # Add the idle time
                print(f"Recorded {elapsed_time} seconds of idle time.")
                self.start_time = None  # Reset the start time
            time.sleep(60)  # Check for idle time every minute
            print(f"Total screen time so far is {self.total_time} seconds.")
            try:
                print("About to write to file.")
                with open('screen_time.txt', 'a') as f:
                    hours, rem = divmod(self.total_time, 3600)
                    minutes, seconds = divmod(rem, 60)
                    f.write(f"Total screen time so far is {int(hours)}:{int(minutes)}:{int(seconds)}.\n")
                print("Finished writing to file.")

            except IOError as e:
                print(f"An error occurred while writing to file: {e}")

            except Exception as e:
                print(f"An unexpected error occurred: {e}")


tracker = ScreenTimeTracker()
