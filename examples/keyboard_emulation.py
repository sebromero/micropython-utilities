from machine import Pin
from micropython_utilities import KeyboardEmulator, KeyCode
from time import sleep_ms

btn_up = Pin("D2", Pin.IN)
btn_down = Pin("D3", Pin.IN)

virtual_keyboard = KeyboardEmulator()
virtual_keyboard.add_binding(lambda: not btn_up.value(), KeyCode.UP)
virtual_keyboard.add_binding(lambda: not btn_down.value(), KeyCode.DOWN)
virtual_keyboard.start()

# Keys can also be sent standalone
# virtual_keyboard.send_keys([KeyCode.SPACE])

while True:
    virtual_keyboard.update()
    sleep_ms(1)