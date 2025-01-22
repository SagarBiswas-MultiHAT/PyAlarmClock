
# Python Alarm Clock

A simple Python-based alarm clock application that uses the system's current time to trigger an alarm. The alarm plays an audio file (`alarm.wav`) until stopped by the user.

## Features

- **Set Alarm**: Users can input the alarm time in `HH:MM:SS AM/PM` format.
- **Audio Notification**: Plays an audio file (`alarm.wav`) when the alarm time is reached.
- **Live Time Display**: Displays the current time in real-time.
- **Interrupt Handling**: Gracefully stops the program with `Ctrl+C`.

## Requirements

- Python 3.x
- `winsound` (available only on Windows)
- An audio file named `alarm.wav` in the same directory as the script.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SagarBiswas-MultiHAT/python-alarm-clock.git
   ```
2. Navigate to the project directory:
   ```bash
   cd python-alarm-clock
   ```
3. (Optional) Set up a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # For Windows
   ```
4. No additional libraries are required to install, as `winsound` is built into Python on Windows.

## Usage

1. Run the script:
   ```bash
   python script.py
   ```
2. Enter the alarm time when prompted (e.g., `07:30:00 AM`).
3. The program will play the alarm sound (`alarm.wav`) when the set time is reached.
4. Stop the alarm or exit the program using `Ctrl+C`.

## Notes

- Ensure the `alarm.wav` file exists in the same directory as the script.
- The program is designed for Windows due to the use of the `winsound` module.

## Example

Input: `07:30:00 AM`

Output:

- Displays real-time updates of the current system time.
- Plays the `alarm.wav` file repeatedly at `07:30:00 AM`.


---

#### Contributions are welcome! Feel free to open issues or submit pull requests.

