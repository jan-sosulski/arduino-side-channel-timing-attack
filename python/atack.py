import serial
import time
import csv
import numpy as np
from tqdm import tqdm

MODULUS = 3233
PUBLIC_KEY = 17
MAX_BITS = 6
MEASUREMENTS = 1  # Number of measurements for each message
SIM_ROWS = 100000  # Number of rows in the simulation data
SIM_MAX_AGE = 3600  # Maximum age of the simulation data in seconds


def modular_exponentiation(base: int, exp: int, flag: int):
    ans = 1
    for i in range(32):
        if i > flag:
            return ans % MODULUS
        if (exp >> i) & 1:
            ans = (ans * base) % MODULUS
        base = (base * base) % MODULUS
    return ans % MODULUS


def measure_time(serial_port, message):
    """Send a message to Arduino and measure the response time."""
    start_time = time.time_ns()
    serial_port.write(f"{message}\n".encode())
    response = serial_port.readline().decode().strip()
    elapsed_time = time.time_ns() - start_time
    return float(response), elapsed_time


def remove_outliers(data):
    """Remove outliers from a list of data using 2 standard deviations."""
    mean = np.mean(data)
    std_dev = np.std(data)
    return [x for x in data if (mean - 2 * std_dev) < x < (mean + 2 * std_dev)]


def generate_simulation_data(serial_port, max_age_seconds=SIM_MAX_AGE):
    """Generate timing data for the encryption process if not already available or outdated."""
    import os
    import time

    if os.path.exists("simulations.csv"):
        file_age = time.time() - os.path.getmtime("simulations.csv")
        if file_age < max_age_seconds:
            with open("simulations.csv", 'r') as sim_file:
                rows = list(csv.reader(sim_file))
                if len(rows) == SIM_ROWS:
                    print("Simulation data is recent and consistent. Skipping generation.")
                    return
        print("Simulation data is outdated or incomplete. Regenerating...")

    print("Generating simulation data...")
    with open("simulations.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for message in tqdm(range(SIM_ROWS), desc="Generating Simulation Data"):
            try:
                _, time_elapsed = measure_time(serial_port, f"{message}")
                csv_writer.writerow([time_elapsed])
            except Exception as e:
                print(f"Error during data generation for message {message}: {e}")


def deduce_key_bits(serial_port):
    """Deduce key bits based on variance analysis."""
    one_list = []
    zero_list = []

    # Timing for guessed bit 1
    for message in tqdm(range(SIM_ROWS), desc="Analyzing guessed bit 1"):
        for _ in range(MEASUREMENTS):
            _, time_elapsed = measure_time(serial_port, f"{message}")
            one_list.append(time_elapsed)

    # Timing for guessed bit 0
    for message in tqdm(range(SIM_ROWS), desc="Analyzing guessed bit 0"):
        for _ in range(MEASUREMENTS):
            _, time_elapsed = measure_time(serial_port, f"{message}")
            zero_list.append(time_elapsed)

    # one_list = remove_outliers(one_list)
    # zero_list = remove_outliers(zero_list)

    with open("simulations.csv", 'r') as sim:
        siml = list(csv.reader(sim))
        if len(siml) != SIM_ROWS:
            print(f"Expected {SIM_ROWS} rows, found {len(siml)}. Regenerating data...")
            generate_simulation_data(serial_port)
            return deduce_key_bits(serial_port)

        for i in range(len(siml)):
            one_list[i] = float(siml[i][0]) - one_list[i]
            zero_list[i] = float(siml[i][0]) - zero_list[i]

    zero_variance = np.var(zero_list)
    one_variance = np.var(one_list)

    print("Zero's Variance =", zero_variance)
    print("One's Variance =", one_variance)

    return 0 if zero_variance < one_variance else 1



def kocher_attack(serial_port, max_bits):
    """Perform Kocher's Timing Attack to deduce the private key."""
    guessed_key = []

    with open("kocher_results.csv", 'w', newline='') as result_file:
        csv_writer = csv.writer(result_file)
        csv_writer.writerow(["Bit Position", "Guessed Bit"])

        for bit_position in tqdm(range(max_bits), desc="Kocher's Timing Attack"):
            print(f"Analyzing bit {bit_position + 1}...")
            key_bit = deduce_key_bits(serial_port)
            guessed_key.append(key_bit)

            # Save progress after each bit
            csv_writer.writerow([bit_position + 1, key_bit])
            result_file.flush()

            print(f"Bit {bit_position + 1}: {key_bit}")

    private_key = int(''.join(map(str, guessed_key)), 2)
    print(f"Guessed Private Key: {private_key}")
    return private_key


if __name__ == "__main__":
    SERIAL_PORT = "COM5"  # Replace with your Arduino's serial port
    BAUD_RATE = 115200

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as arduino:
            time.sleep(4)  # Allow Arduino to reset
            print("Generating simulation data...")
            generate_simulation_data(arduino)

            print("Starting Kocher's Timing Attack...")
            guessed_key = kocher_attack(arduino, MAX_BITS)
            print(f"Deduced Private Key: {guessed_key}")
    except Exception as e:
        print(f"Error: {e}")
