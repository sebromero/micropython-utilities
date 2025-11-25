"""
This example demonstrates basic usage of the Serial class to communicate over USB-CDC.
This is useful for interacting with the device via a serial terminal on the host computer.

For example you can run a python application on the host that reads sensor data from the device
and displays it in real-time.
"""
from machine import Pin
from micropython_utilities import Serial
from time import sleep_ms

led = Pin("LED_BUILTIN", Pin.OUT)
ser = Serial()
ser.begin()

while not ser.connected:
    print("Waiting for host to connect...")
    led.value(not led.value())
    sleep_ms(250)

led.on() # Turn on LED to indicate connection established
ser.println("Connected! You can start sending data.")

while True:
    line = ser.readline()
    if line:
        print("Received:", line)
        ser.println("Echo: " + line) # Echo back to host