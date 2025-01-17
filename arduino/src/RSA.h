#pragma once
#include <Arduino.h>

// Example public and private keys (not secure, for educational purposes)
const unsigned long PUBLIC_KEY = 17;     // e
const unsigned long PRIVATE_KEY = 45;  // d
const unsigned long MODULUS = 3233;     // n

unsigned long modExp(unsigned long base, unsigned long exp, unsigned long mod);

unsigned long encrypt(unsigned long message);

unsigned long decrypt(unsigned long encryptedMessage);