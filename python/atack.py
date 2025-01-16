import serial
import time
import statistics

# Połączenie z Arduino przez port szeregowy (dostosuj port)
arduino = serial.Serial('COM3', 9600, timeout=1)  # Zmień 'COM3' na odpowiedni port

# Funkcja do wysyłania ciphertextu do Arduino i odbierania odpowiedzi
def send_to_arduino(ciphertext):
    arduino.write(f"{ciphertext}\n".encode())  # Wysyła ciphertext do Arduino
    start_time = time.time()  # Zaczynaj mierzyć czas
    response = arduino.readline().decode().strip()  # Odbiera odpowiedź (odszyfrowaną wiadomość)
    end_time = time.time()  # Kończymy mierzenie czasu
    response_time = end_time - start_time  # Oblicz czas odpowiedzi
    return response, response_time

# Funkcja przeprowadzająca atak czasowy na RSA
def timing_attack(n, num_trials=100):
    response_times = {}  # Słownik do przechowywania czasów odpowiedzi

    # Przeprowadzamy atak na różne ciphertexty
    for trial in range(num_trials):
        print(f"Trial {trial + 1}/{num_trials}")
        
        # Testujemy różne ciphertexty (tutaj zakładając, że są małe liczby)
        for i in range(1, n):
            print(f"Testing ciphertext: {i}")
            response, response_time = send_to_arduino(i)  # Wysyłamy do Arduino i otrzymujemy czas odpowiedzi

            # Zapisujemy czas odpowiedzi dla każdego ciphertextu
            if i not in response_times:
                response_times[i] = []
            response_times[i].append(response_time)

    # Obliczamy średnie i odchylenie standardowe czasów odpowiedzi dla każdego ciphertextu
    avg_response_times = {}
    std_dev_response_times = {}
    
    for ciphertext, times in response_times.items():
        avg_response_times[ciphertext] = statistics.mean(times)
        std_dev_response_times[ciphertext] = statistics.stdev(times) if len(times) > 1 else 0

    # Określamy próg na podstawie średnich czasów odpowiedzi
    avg_time = statistics.mean(avg_response_times.values())
    std_dev_time = statistics.stdev(avg_response_times.values()) if len(avg_response_times) > 1 else 0
    threshold = avg_time + std_dev_time  # Proporcja do średniego czasu odpowiedzi
    
    print(f"\nCalculated threshold: {threshold:.6f} seconds (mean + stddev)")

    # Analizujemy czasy odpowiedzi i próbujemy odgadnąć bity klucza
    potential_private_key = []
    for i in range(1, n):
        avg_time_for_cipher = avg_response_times[i]
        if avg_time_for_cipher > threshold:  # Jeśli czas jest większy od progu, to przypisujemy bit 1
            potential_private_key.append(1)
        else:
            potential_private_key.append(0)

    # Rekonstrukcja klucza prywatnego
    print("Reconstructed private key bits:")
    reconstructed_key = ''.join(map(str, potential_private_key))
    print(f"Private key (approx.): {reconstructed_key}")

# Zakładając publiczny klucz (e, n)
n = 3233  # Modulus (n = p * q dla prostych p i q)
e = 17    # Publiczny eksponent (często używany w RSA)

# Uruchomienie ataku
timing_attack(n, num_trials=2)
