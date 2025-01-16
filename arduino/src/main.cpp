#include <Arduino.h>

#include <Arduino.h>

long long mod_exp(long long base, long long exponent, long long modulus) {
    long long result = 1;
    base = base % modulus;  // Redukcja bazy

    while (exponent > 0) {
        if (exponent % 2 == 1) {  // Jeśli bit wykładnika to 1, wykonaj mnożenie
            result = (result * base) % modulus;
        }
        exponent = exponent >> 1;  // Przesuń wykładnik w prawo
        base = (base * base) % modulus;  // Kwadrat bazy
    }

    return result;
}

void setup() {
    Serial.begin(9600);  // Uruchomienie komunikacji szeregowej

    long long n = 3233;  // Modulus (n = p * q dla prostych p i q)
    long long d = 2753;  // Klucz prywatny (d)
    
    // Przykładowa wiadomość do deszyfrowania
    long long ciphertext = 1234;  

    long long start_time = millis();  // Zaczynamy pomiar czasu
    long long decrypted = mod_exp(ciphertext, d, n);  // Deszyfrowanie wiadomości
    long long end_time = millis();  // Kończymy pomiar czasu

    long long execution_time = end_time - start_time;  // Czas wykonania operacji

    Serial.print("Decrypted message: ");
    Serial.println(decrypted);
    Serial.print("Execution time (ms): ");
    Serial.println(execution_time);  // Wyświetlanie czasu wykonania operacji

    // Możemy teraz przeprowadzić atak czasowy, mierząc czas wykonania
}

void loop() {
    // W pętli nie wykonujemy żadnych działań, czekamy na komunikację z Pythonem
}
