from machine import Pin
from time import sleep_ms
from micropython_utilities import Dimmer

led = Pin("LED_BUILTIN", Pin.OUT)  # Use the built-in LED pin
dimmer = Dimmer(led)  # Initialize Dimmer

for brightness in range(0, 101, 10):  # Increase brightness from 0 to 100
    dimmer.brightness = brightness
    print(f"Brightness set to: {brightness}%")
    sleep_ms(50)  # Wait for 100 milliseconds

for brightness in range(100, -1, -10):  # Decrease brightness from 100 to 0
    dimmer.brightness = brightness
    print(f"Brightness set to: {brightness}%")
    sleep_ms(50)  # Wait for 100 milliseconds