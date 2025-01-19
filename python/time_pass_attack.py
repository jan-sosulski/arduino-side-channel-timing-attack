import time
import statistics

# Symulowana funkcja check (imitująca wyciek czasowy)
def check(input_password):
    in_memory_password = "secret"  # Hasło zapisane w pamięci
    for i in range(len(in_memory_password)):
        if input_password[i] != in_memory_password[i]:
            return 0  # Przerwanie natychmiastowe
        # add 1 s delay
        time.sleep(0.0001)
    return 1

# Funkcja do mierzenia medianowego czasu wykonania
def measure_median_time(input_password, repetitions=1):
    times = []
    for _ in range(repetitions):
        start = time.perf_counter_ns()
        check(input_password)
        end = time.perf_counter_ns()
        times.append(end - start)
    return statistics.median(times)  # Liczymy medianę

# Atak side-channel: odgadywanie hasła bajt po bajcie
def timing_attack():
    known_password = ""  # Odkrywane hasło
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Możliwe znaki

    for _ in range(6):  # Zakładamy długość hasła 6 znaków
        timings = []
        for char in charset:
            test_password = known_password + char + "A" * (5 - len(known_password))  # Padding
            exec_time = measure_median_time(test_password, repetitions=50)  # Mierzymy medianę czasu
            timings.append((char, exec_time))

        # Wybieramy znak z najdłuższym medianowym czasem wykonania
        best_char = max(timings, key=lambda x: x[1])[0]
        known_password += best_char
        print(f"Odgadnięty dotychczasowy ciąg: {known_password}")

    return known_password

# Uruchamiamy atak
recovered_password = timing_attack()
print(f"Odgadnięte hasło: {recovered_password}")
