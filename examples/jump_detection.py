from modulino import ModulinoMovement
from micropython_utilities import JumpDetector

movement = ModulinoMovement()
threshold = 1.75  # Threshold (in g) for jump detection
jump_detector = JumpDetector(threshold)
jump_detector.on_jump = lambda avg: print(f"Jump detected! 📈 Avg.: {avg:>8.3f}\n")

while True:
    jump_detector.append(movement.acceleration)
    jump_detector.update()