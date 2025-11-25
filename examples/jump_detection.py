from modulino import ModulinoMovement
from micropython_utilities import JumpDetector

movement = ModulinoMovement()
sample_rate = 25  # Only insert a new sample every 25 ms
buffer_size = 10  # Store the last 10 samples
threshold = 1.75  # Threshold (in g) for jump detection
jump_detector = JumpDetector(buffer_size, threshold, sample_rate)
jump_detector.on_jump = lambda avg: print(f"Jump detected! 📈 Avg.: {avg:>8.3f}\n")

while True:
    jump_detector.append(movement.acceleration)
    jump_detector.update()