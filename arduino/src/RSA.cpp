#include "RSA.h"


// Function to perform modular exponentiation
unsigned long modExp(unsigned long base, unsigned long exp, unsigned long mod) {
    unsigned long result = 1;
    base = base % mod;
    while (exp > 0) {
        if (exp % 2 == 1) {
            result = (result * base) % mod;
        }
        exp = exp >> 1;
        base = (base * base) % mod;
    }
    return result;
}

// RSA encryption function
unsigned long encrypt(unsigned long message) {
    return modExp(message, PUBLIC_KEY, MODULUS);
}

// RSA decryption function
unsigned long decrypt(unsigned long encryptedMessage) {
    return modExp(encryptedMessage, PRIVATE_KEY, MODULUS);
}
