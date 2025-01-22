from datetime import datetime   
import winsound
import time

# Display the current time at the start of the program
now = datetime.now()
current_time = now.strftime("%I:%M:%S %p")
print("\n\t..:: Current Time at Start:", current_time)

alarm_time = input("\n\t..:: Enter the time of alarm to be set (HH:MM:SS AM/PM) ==> ")
alarm_hour = alarm_time[0:2]
alarm_minute = alarm_time[3:5]
alarm_seconds = alarm_time[6:8]
alarm_period = alarm_time[9:11].upper()
print("\n\n\t\t\t..:: Setting up alarm ::..")

try:
    while True:
        now = datetime.now()
        current_time = now.strftime("%I:%M:%S %p")
        print("\n\n\t ==> Current Time:", current_time, end="\r") # \r is used to print the output in the same line
        current_hour = now.strftime("%I")
        current_minute = now.strftime("%M")
        current_seconds = now.strftime("%S")
        current_period = now.strftime("%p")
        
        if (alarm_period == current_period and
            alarm_hour == current_hour and
            alarm_minute == current_minute and
            alarm_seconds == current_seconds):
            print("Wake Up!")
            while True:
                winsound.PlaySound('alarm.wav', winsound.SND_FILENAME)
                time.sleep(1)
        
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n\t\t\t..:: Alarm Stopped ::..\n\n")

# Correct virtual environment activation command for Windows

        # python -m venv venv
        # venv\Scripts\activate
        # pip install winsound
