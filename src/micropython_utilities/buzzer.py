from machine import PWM, Pin
from time import sleep_ms

class Buzzer:
  """
  Predefined notes are available in the NOTES dictionary e.g. Buzzer.NOTES["C4"]
  Class to play tones on the piezo element of the Buzzer.
  """

  NOTES: dict[str, int] = {
    "FS3": 185,
    "G3": 196,
    "GS3": 208,
    "A3": 220,
    "AS3": 233,
    "B3": 247,
    "C4": 262,
    "CS4": 277,
    "D4": 294,
    "DS4": 311,
    "E4": 330,
    "F4": 349,
    "FS4": 370,
    "G4": 392,
    "GS4": 415,
    "A4": 440,
    "AS4": 466,
    "B4": 494,
    "C5": 523,
    "CS5": 554,
    "D5": 587,
    "DS5": 622,
    "E5": 659,
    "F5": 698,
    "FS5": 740,
    "G5": 784,
    "GS5": 831,
    "A5": 880,
    "AS5": 932,
    "B5": 988,
    "C6": 1047,
    "CS6": 1109,
    "D6": 1175,
    "DS6": 1245,
    "E6": 1319,
    "F6": 1397,
    "FS6": 1480,
    "G6": 1568,
    "GS6": 1661,
    "A6": 1760,
    "AS6": 1865,
    "B6": 1976,
    "C7": 2093,
    "CS7": 2217,
    "D7": 2349,
    "DS7": 2489,
    "E7": 2637,
    "F7": 2794,
    "FS7": 2960,
    "G7": 3136,
    "GS7": 3322,
    "A7": 3520,
    "AS7": 3729,
    "B7": 3951,
    "C8": 4186,
    "CS8": 4435,
    "D8": 4699,
    "DS8": 4978,
    "REST": 0
  }
  """
  Dictionary with the notes and their corresponding frequencies.
  The supported notes are defined as follows:
  - FS3, G3, GS3, A3, AS3, B3
  - C4, CS4, D4, DS4, E4, F4, FS4, G4, GS4, A4, AS4, B4
  - C5, CS5, D5, DS5, E5, F5, FS5, G5, GS5, A5, AS5, B5
  - C6, CS6, D6, DS6, E6, F6, FS6, G6, GS6, A6, AS6, B6
  - C7, CS7, D7, DS7, E7, F7, FS7, G7, GS7, A7, AS7, B7
  - C8, CS8, D8, DS8
  - REST (Silence)
  """

  def __init__(self, pin, duty_cycle=65535 // 8):
    """
    Initializes the Buzzer.

    Parameters:
        pin (str): The pin to which the buzzer is connected.
        duty_cycle (int): The duty cycle for the PWM signal. Default is 12.5% (65535 // 8).
    """
    self._pwm = PWM(Pin(pin))  # Initialize PWM on the specified pin
    self._duty_cycle = duty_cycle
    self.no_tone()

  def tone(self, frequency: int, length_ms: int = 0xFFFF, blocking: bool = False) -> None:
    """
    Plays a tone with the given frequency and duration.
    If blocking is set to True, the function will wait until the tone is finished.

    Parameters:
        frequency: The frequency of the tone in Hz (freuqencies below 180 Hz are not supported)
        lenght_ms: The duration of the tone in milliseconds. If omitted, the tone will play indefinitely
        blocking: If set to True, the function will wait until the tone is finished
    """
    if frequency == 0:
      self.no_tone()
      if blocking:
        sleep_ms(length_ms)
      return

    self._pwm.freq(frequency)
    self._pwm.duty_u16(self._duty_cycle)  # Set duty cycle to 12.5% to produce sound

    if blocking:
      sleep_ms(length_ms)
      self.no_tone()  # Stop the tone after the specified duration

  def no_tone(self) -> None:
    """
    Stops the current tone from playing.
    """
    self._pwm.duty_u16(0)  # Set duty cycle to 0% to stop sound
