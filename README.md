# Arduino side channel timing attack

## Overview
This project demonstrates a timing side-channel attack on a microcontroller based password protected system. 
The attack exploits the implementation of string comparison, which shows a high correlation between execution time and the number of iterations.

## Folder Structure
```
Arduino side channel timing attack/
├── arduino/
├── python/
├── stm/
└── README.md
```

## Files and Directories
- **arduino/**: Contains Arduino code with a sample implementation of the side-channel attack.
- **python/**: Contains Python scripts for attack execution. It also contains concept code for the attack.
- **stm/**: STM32L476RG-based high-resolution timer module designed for precise time measurement and pulse width analysis.

## Attack Process
1. **Deploy the Arduino code**: Upload the Arduino code to the target device. We use PlatformIO to upload the code to the Arduino.

2. **Use STM as a high-resolution timer**: Connect the STM32L476RG to the target device output pin and use it as a high-resolution timer. REMEMBER that arduino works at 5V and STM32L476RG works at 3.3V. Use a voltage divider to connect the output pin to the STM32L476RG. You can also connect diode to the output pin to see when messages are sent.

3. **Run the Python script**: Run the Python script to perform the side-channel attack. The script will collect the time taken for each iteration and analyze the correlation between the execution time and the number of iterations. Remember to change the serial ports number in the script. Script synchronizes messages to Arduino and STM32L476RG.