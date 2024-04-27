import time
import pygame

# Initialize the pygame mixer
pygame.mixer.init()

# Define work and break durations in seconds
WORK_DURATION = 1 * 60  # 25 minutes
SHORT_BREAK_DURATION = 5 * 60  # 5 minutes
LONG_BREAK_DURATION = 2 * 60  # 15 minutes

# Define the sound file to play at the end of each period
# Make sure you have a sound file in the same directory as the script or provide the path to the sound file
SOUND_FILE = 'alarmtone.mp3'  # Replace 'alarm.mp3' with the path to your sound file


def play_sound():
    # Load and play the sound file
    pygame.mixer.music.load(SOUND_FILE)
    pygame.mixer.music.play()
    # Wait until the sound finishes playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)


def pomodoro_timer():
    # Initialize cycle count and long break interval
    cycle_count = 0
    long_break_interval = 4  # Number of cycles before a long break

    # Run the Pomodoro timer loop
    while True:
        # Increment cycle count
        cycle_count += 1

        # Work period
        print("Work period: 25 minutes")
        time.sleep(WORK_DURATION)
        print("Work period over")
        play_sound()  # Play sound notification

        # Check if it's time for a long break
        if cycle_count % long_break_interval == 0:
            # Long break period
            print("Long break period: 15 minutes")
            time.sleep(LONG_BREAK_DURATION)
            print("Long break period over")
        else:
            # Short break period
            print("Short break period: 5 minutes")
            time.sleep(SHORT_BREAK_DURATION)
            print("Short break period over")

        # Play sound notification
        play_sound()


if __name__ == "__main__":
    # Start the Pomodoro timer
    pomodoro_timer()