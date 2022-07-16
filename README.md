# pottery-wheel-control
This repository is Micropython code for Raspberry Pi Pico 
for controlling a DIY pottery wheel.

This project supports:
 - Setting max RPM via 24 pin encoder
 - Setting current speed (0-max speed) with foot pedal (10K potentiometer)
 - Realtime speed control feedback loop:
   - Measure speed
   - Aim to RPM - will keep RPM also under load
 - Reverse switch (will cause complete stop before reversing)