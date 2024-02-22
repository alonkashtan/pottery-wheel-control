# pottery-wheel-control
This repository is Micropython code for Raspberry Pi Pico 
for controlling a DIY pottery wheel.

This project supports:
 - Setting max RPM via 24 pin encoder + presets button
 - Setting current speed (0-max RPM) with foot pedal
 - Speed control via servo (connected to a speed controller)
 - Realtime speed control feedback loop:
   - Measure speed
   - PID was not actually implemented since the motor is strong enough to keep RPM in any reasonable load
 - Switching motor on/off using relay
 - LCD to show max/requested/current RPM

The rotary encoder module would be interesting for many - it is based on an example I found, but is the only 
implementation I found that catches every click in the rotary encoder. 