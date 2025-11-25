# This example demonstrates the usage of the Timer class to 
# toggle two LEDs at different intervals.

from micropython_utilities import Timer
from machine import Pin
from time import sleep_ms

led_r = Pin("LEDR")
led_b = Pin("LEDB")

def toggle_led_r():
    led_r.value(not led_r.value())

def toggle_led_b():
    led_b.value(not led_b.value())

t1 = Timer(1000, False) # 1 second interval
# Register the callback function to toggle the red LED
t1.on_timer_end = toggle_led_r
t1.start()

t2 = Timer(600, False) # 0.6 second interval
# Register the callback function to toggle the blue LED
t2.on_timer_end = toggle_led_b
t2.start() # Sets the start time

t3 = Timer(2000, True) # 2 second one-shot timer
t3.on_timer_end = lambda: print("Timer 3 ended after 2 seconds")
t3.start()

while True:
    t1.update()
    t2.update()
    t3.update()
    print(f"Timer 1 elapsed: {t1.elapsed_ms} ms")
    print(f"Timer 2 elapsed: {t2.elapsed_ms} ms")
    sleep_ms(100)
