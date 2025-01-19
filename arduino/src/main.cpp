#include <Arduino.h>

String password = "password";
String potential_password = "0000000";
void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        
        // get potential password from serial, read till newline
        potential_password = Serial.readStringUntil('\n');

        // check the password byte by byte
        digitalWrite(LED_BUILTIN, HIGH);
        // for (int j = 0; j < password.length(); j++) {
        //     if (password[j] != potential_password[j]) {
        //         digitalWrite(LED_BUILTIN, LOW);
        //         Serial.println("Incorrect password");
        //         break;
        //     }
        // }
        if (password == potential_password) {
            digitalWrite(LED_BUILTIN, LOW);
            Serial.println("Correct password");
        } else {
            digitalWrite(LED_BUILTIN, LOW);
            Serial.println("Incorrect password");
        }
        // digitalWrite(LED_BUILTIN, LOW);
        while (Serial.available() > 0) {
            Serial.read();
        }
    }
    
}
