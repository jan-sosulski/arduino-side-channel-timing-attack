# KRYS Side Channel Attack

## Overview
This project demonstrates a timing side-channel attack on a microcontroller based password protected system. 
The attack exploits the implementation of string comparison, which shows a high correlation between execution time and the number of iterations.

## Folder Structure
```
KRYS-side-channel-attack/
├── arduino/
├── python/
├── stm/
└── README.md
```

## Files and Directories
- **arduino/**: Contains Arduino code with a sample implementation of the side-channel attack.
- **python/**: Contains Python scripts for attack execution.
- **stm/**: STM32L476RG-based high-resolution timer module designed for precise time measurement and pulse width analysis.
