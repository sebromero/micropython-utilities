from machine import PWM

class Dimmer:
    def __init__(self, pin, freq=1000):
        self.pin = pin
        self.freq = freq
        self._brightness = 0
        self.pwm = PWM(pin, freq=freq, duty_u16=0) 

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        if value < 0 or value > 100:
            raise ValueError("Brightness must be between 0 and 100")
        self._brightness = value
        duty = int(value * 65535 / 100)
        
        if self.pwm is not None:
            self.pwm.duty_u16(duty)

    def __del__(self):
        if self.pwm is not None:
            self.pwm.deinit()
            self.pwm = None