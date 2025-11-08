# This script provides a class that detects jumps using the accelerometer data.
# It uses a deque to store the last N motion vector magnitudes. It works in a similar way to the RingBuffer class.
# It also includes a callback that is called when a jump is detected.
# You need to call the append method with the accelerometer data and the update method in a loop to detect jumps.
# The data sampling works without using sleep_ms, so it can be used in a non-blocking way.

from math import sqrt
from time import ticks_ms, ticks_diff
from collections import deque

class JumpDetector:
    MIN_JUMP_INTERVAL = 500 # Minimum time between jumps in milliseconds

    def __init__(self, buffer_size, threshold, sample_rate):
        self.size = buffer_size # Size of the buffer to hold the last N motion vector magnitudes
        self.data = deque([], buffer_size) # Prefill the buffer with zeros
        self.threshold = threshold # Motion vector magnitude threshold for jump detection
        self._last_jump_detected_time = 0 # Time when the last jump was detected
        self._sample_rate = sample_rate # Sample rate in milliseconds
        self._last_sample_inserted_time = 0 # Time when the last sample was inserted

    @property
    def on_jump(self):
        return self._on_jump
    
    @on_jump.setter
    def on_jump(self, callback):
        self._on_jump = callback

    def _calculate_motion_vector_magnitude(self, accel_data):
        """
        Calculate the magnitude of the motion vector.
        This is the square root of the sum of the squares of the x, y, and z
        components of the acceleration vector. See: https://www.cuemath.com/magnitude-of-a-vector-formula/
        """
        return sqrt(accel_data[0]**2 + accel_data[1]**2 + accel_data[2]**2)

    def append(self, accel_values):
        current_time = ticks_ms()
        time_since_last_sample_insert = ticks_diff(current_time, self._last_sample_inserted_time)
        
        # Only insert a new sample if the sample rate has passed
        if time_since_last_sample_insert < self._sample_rate:
            return
        
        magnitude = self._calculate_motion_vector_magnitude(accel_values)
        self.data.append(magnitude)
        self._last_sample_inserted_time = current_time

    def _average(self):
        return sum(self.data) / len(self.data)

    def update(self):
        average = self._average()
        is_jump = average > self.threshold
        time_since_last_jump = ticks_diff(ticks_ms(), self._last_jump_detected_time)
        
        # Execute the callback if a jump is detected and the minimum jump interval has passed
        if is_jump and time_since_last_jump > self.MIN_JUMP_INTERVAL:
            self._last_jump_detected_time = ticks_ms()
            if self._on_jump:
                self._on_jump(average)

if __name__ == "__main__":
    from modulino import ModulinoMovement
    movement = ModulinoMovement()
    sample_rate = 25  # Only insert a new sample every 25 ms
    buffer_size = 10  # Store the last 10 samples
    threshold = 1.75  # Threshold (in g) for jump detection
    jump_detector = JumpDetector(buffer_size, threshold, sample_rate)
    jump_detector.on_jump = lambda avg: print(f"Jump detected! 📈 Avg.: {avg:>8.3f}\n")

    while True:
        jump_detector.append(movement.accelerometer)
        jump_detector.update()