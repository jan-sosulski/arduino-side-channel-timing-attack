import time
import statistics

# Simulated check function (imitating a timing leak)
def check(input_password):
    in_memory_password = "secret"  # Password stored in memory
    for i in range(len(in_memory_password)):
        if input_password[i] != in_memory_password[i]:
            return 0  # Immediate termination
        # add 1 ms delay
        time.sleep(0.0001)
    return 1

# Function to measure median execution time
def measure_median_time(input_password, repetitions=1):
    times = []
    for _ in range(repetitions):
        start = time.perf_counter_ns()
        check(input_password)
        end = time.perf_counter_ns()
        times.append(end - start)
    return statistics.median(times)  # Calculate median

# Side-channel attack: guessing the password byte by byte
def timing_attack():
    known_password = ""  # Discovered password
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Possible characters

    for _ in range(6):  # Assuming password length of 6 characters
        timings = []
        for char in charset:
            test_password = known_password + char + "A" * (5 - len(known_password))  # Padding
            exec_time = measure_median_time(test_password, repetitions=50)  # Measure median time
            timings.append((char, exec_time))

        # Select the character with the longest median execution time
        best_char = max(timings, key=lambda x: x[1])[0]
        known_password += best_char
        print(f"Discovered so far: {known_password}")

    return known_password

# Run the attack
recovered_password = timing_attack()
print(f"Discovered password: {recovered_password}")
