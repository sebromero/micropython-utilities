from micropython_utilities import Buzzer

buzzer = Buzzer("D8") # Connect the buzzer to pin D8

# Super Mario Bros theme intro
melody = [
    (Buzzer.NOTES["E5"], 125),
    (Buzzer.NOTES["REST"], 25),
    (Buzzer.NOTES["E5"], 125),
    (Buzzer.NOTES["REST"], 125),
    (Buzzer.NOTES["E5"], 125),
    (Buzzer.NOTES["REST"], 125),
    (Buzzer.NOTES["C5"], 125),
    (Buzzer.NOTES["E5"], 125),
    (Buzzer.NOTES["REST"], 125),
    (Buzzer.NOTES["G5"], 125),
    (Buzzer.NOTES["REST"], 375),
    (Buzzer.NOTES["G4"], 250)
]

for note, duration in melody:
    buzzer.tone(note, duration, blocking=True)