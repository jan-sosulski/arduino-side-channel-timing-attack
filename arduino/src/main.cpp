#include <Arduino.h>
#include "RSA.h"


void setup() {
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        String input = Serial.readStringUntil('\n');
        input.trim();

        unsigned long message = input.toInt();
        unsigned long encryptedMessage = encrypt(message);
        Serial.println(encryptedMessage);
    }
}
