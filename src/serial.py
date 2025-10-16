# Author: Sebastian Romero
# This module provides a USB-CDC serial interface over USB

import time
import usb.device
from usb.device.cdc import CDCInterface

class Serial:
    def __init__(self):
        self.cdc = CDCInterface()
        self.cdc.init(timeout=0)  # zero timeout makes this non-blocking, suitable for os.dupterm()

    def begin(self) -> None:
        # pass builtin_driver=True so that we get the built-in USB-CDC alongside, if it's available.
        usb.device.get().init(self.cdc, builtin_driver=True)

        # wait for host enumerate as a CDC device...
        while not self.cdc.is_open():
            time.sleep_ms(100)

    def write(self, data) -> None:
        self.cdc.write(data)

    def read(self, nbytes=None) -> bytes:
        return self.cdc.read(nbytes)

    def readline(self) -> str:
        line = bytearray()
        while True:
            char = self.cdc.read(1)
            if not char or char == b'\n':
                break
            line += char
        return line.decode()
    
    @property
    def connected(self) -> bool:
        # Wait for the host to connect to the new serial port (e.g. open a terminal program)
        return self.cdc.dtr  # Data Terminal Ready signal
    
    @property
    def available_bytes(self) -> int:
        return self.cdc._rb.readable()
    
if __name__ == "__main__":
    ser = Serial()
    ser.begin()

    while not ser.connected:
        print("Waiting for host to connect...")
        time.sleep_ms(100)

    while True:
        line = ser.readline()
        if line:
            print("Received:", line)
            ser.write(b'Echo: ' + line + b'\n')