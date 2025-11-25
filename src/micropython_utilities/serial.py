# Author: Sebastian Romero
# This module provides a USB-CDC serial interface over USB

from time import sleep_ms
import usb.device
from usb.device.cdc import CDCInterface

class Serial:
    def __init__(self):
        self.cdc = CDCInterface()
        self.cdc.init(timeout=0)  # zero timeout makes this non-blocking, suitable for os.dupterm()

    def begin(self) -> None:
        """Initializes the USB-CDC serial interface and waits for the host to enumerate."""
        # pass builtin_driver=True so that we get the built-in USB-CDC alongside, if it's available.
        usb.device.get().init(self.cdc, builtin_driver=True)

        # wait for host enumerate as a CDC device...
        while not self.cdc.is_open():
            sleep_ms(100)

    def write(self, data: bytes) -> None:
        self.cdc.write(data)

    def print(self, message: str) -> None:
        self.write(message.encode())
    
    def println(self, message: str) -> None:
        self.print(message + '\n')

    def read(self, nbytes=-1) -> bytes:
        """Reads up to nbytes from the serial input buffer. If nbytes is -1, reads all available bytes."""
        return self.cdc.read(nbytes)

    def readline(self) -> str:
        """Reads a line from the serial input until a newline character is encountered."""
        line = bytearray()
        while True:
            char = self.cdc.read(1)
            if not char or char == b'\n':
                break
            line += char
        return line.decode()
    
    @property
    def connected(self) -> bool:
        """
        Returns True if the host is connected to the serial port (e.g. a terminal program is open).
        """
        return self.cdc.dtr  # Data Terminal Ready signal
    
    def __bool__(self) -> bool:
        return self.connected

    @property
    def available_bytes(self) -> int:
        """
        Returns the number of bytes available to read from the serial input buffer.
        """
        return self.cdc._rb.readable()
