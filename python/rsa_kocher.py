import time
import csv
import numpy as np
from tqdm import tqdm  # Importowanie tqdm

# Implementacja modularnej eksponentacji z opóźnieniem
def mod_exp(base, exp, mod, flag):
    ans = 1
    for i in range(0, 32):
        if(i>flag):return ans%mod
        if((exp>>i)&1):
            ans = (ans * base)%mod
        else:
            None
        base = (base * base)%mod
    return ans%mod

# Symulowana funkcja RSA decryption - klucz pozostaje STAŁY
def decrypt_device(ciphertext, flag):
    return mod_exp(ciphertext, PRIVATE_KEY, MODULUS, flag)

def decrypt(ciphertext, private_key, flag):
    return mod_exp(ciphertext, private_key, MODULUS, flag)

# Symulowana funkcja RSA decryption - klucz pozostaje STAŁY
def encrypt_device(ciphertext, flag):
    return mod_exp(ciphertext, PUBLIC_KEY, MODULUS, flag)

def encrypt(ciphertext, private_key, flag):
    return mod_exp(ciphertext, private_key, MODULUS, flag)

# Przykładowe dane RSA
PUBLIC_KEY = 31
PRIVATE_KEY = 75871
MODULUS = 94697
N = 100000000

def guess_key_bits(N):
    """Funkcja zgadująca bity klucza na podstawie analizy czasowej."""
    odgadniety_klucz = 0

    # Dla każdego bitu w kluczu
    for j in range(32):  # Zakładając, że klucz ma 32 bity
        oneList = []
        zeroList = []

        # Zgadywanie bitu jako 1
        for i in tqdm(range(1, N), desc=f"Guessing bit {j} as 1", unit="iteration"):
            timeStart = time.time_ns()
            encrypted_text = encrypt(i, odgadniety_klucz + (1 << j), j)  # Dodajemy 1 w odpowiednim bicie
            timeElapsed = time.time_ns() - timeStart
            oneList.append(timeElapsed)

        # Zgadywanie bitu jako 0
        for i in tqdm(range(1, N), desc=f"Guessing bit {j} as 0", unit="iteration"):
            timeStart = time.time_ns()
            encrypted_text = encrypt(i, odgadniety_klucz, j)  # Nie zmieniamy bitu
            timeElapsed = time.time_ns() - timeStart
            zeroList.append(timeElapsed)

        # Wczytanie danych z pliku simulations.csv
        with open("simulations.csv", 'r') as sim:
            siml = list(csv.reader(sim))
            for i in range(0, N - 1):
                oneList[i] = int(siml[i][0]) - oneList[i]
                zeroList[i] = int(siml[i][0]) - zeroList[i]

        # Obliczanie wariancji
        variance_one = np.var(oneList)
        variance_zero = np.var(zeroList)

        print(f"Zero's Variance for bit {j} = ", variance_zero)
        print(f"One's Variance for bit {j}  = ", variance_one)

        # Zgadywanie bitu na podstawie wariancji
        print(f"Key bit at position {j}: ", 0 if variance_zero < variance_one else 1)

        # Zaktualizowanie odgadniętego klucza
        if variance_zero < variance_one:
            odgadniety_klucz |= (0 << j)  # Bit 0 na pozycji j
        else:
            odgadniety_klucz |= (1 << j)  # Bit 1 na pozycji j

    print("Final guessed key:", bin(odgadniety_klucz))



if __name__ == "__main__":
    with open("simulations.csv", 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        for i in tqdm(range(1,N), desc="CSV generation", unit="iteration"):
            timeStart = time.time_ns()
            # plaintext = i
            # public_key = 31
            # flag = 32 (assuming the public key is of 32 bits)
            encrypted_text = encrypt_device(i, 32)
            timeElapsed = time.time_ns() - timeStart
            csvWriter.writerow([timeElapsed])

    guess_key_bits(N)