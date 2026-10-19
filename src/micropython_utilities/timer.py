from time import ticks_diff, ticks_ms

class Timer:
    def __init__(self, duration_ms=None, one_shot=True):
        """
        Initialize a new Timer instance.

        :param duration_ms: Duration of the timer in milliseconds. If None, the timer has no set duration.
        :param one_shot: If True, the timer will stop after reaching the duration. If False, it will restart automatically.
        """
        self._start_time = None
        self._duration_ms = duration_ms
        self._is_running = False
        self._one_shot = one_shot
        self._on_timer_end = None

    def start(self):
        """
        Start the timer.
        If the timer is already running, this has no effect.
        """
        if self._is_running:
            return
        self._start_time = ticks_ms()
        self._is_running = True

    def reset(self):
        """
        Reset the timer to its initial state.
        The timer will be stopped and the elapsed time will be cleared.
        """
        self._start_time = None
        self._is_running = False        

    def restart(self):
        """
        Restart the timer.
        This will reset the start time to the current time and start the timer.
        """
        self._start_time = ticks_ms()
        self._is_running = True

    def stop(self):
        """
        Stop the timer.
        The timer can be restarted later using the start() or restart() methods.
        """
        self._is_running = False

    @property
    def duration_ms(self):
        """
        Get the duration of the timer in milliseconds.

        :return: The duration of the timer in milliseconds, or None if no duration is set.
        """
        return self._duration_ms
    
    @duration_ms.setter
    def duration_ms(self, value):
        """
        Set the duration of the timer in milliseconds.

        :param value: The duration in milliseconds, or None for no duration.
        :raises ValueError: If the value is negative and not None.
        """
        if value is not None and value < 0:
            raise ValueError("Duration must be non-negative or None.")
        self._duration_ms = value

    @property
    def on_timer_end(self):
        """
        Get the callback function that is called when the timer ends.

        :return: The callback function, or None if no callback is set.
        """
        return self._on_timer_end

    @on_timer_end.setter
    def on_timer_end(self, callback):
        """
        Set the callback function to be called when the timer ends.

        :param callback: A callable function to be called when the timer ends.
        :raises ValueError: If the callback is not callable.
        """
        if not callable(callback):
            raise ValueError("Callback must be callable.")
        self._on_timer_end = callback

    @property
    def elapsed_ms(self):
        """
        Get the elapsed time since the timer was started.

        :return: The elapsed time in milliseconds, or 0 if the timer has not been started.
        """
        if self._start_time is None:
            return 0
        return ticks_diff(ticks_ms(), self._start_time)
    
    @property
    def is_running(self):
        """
        Check if the timer is currently running.

        :return: True if the timer is running, False otherwise.
        """
        return self._is_running

    @property
    def has_ended(self):
        """
        Check if the timer has ended.

        :return: True if the timer has ended, False otherwise.
        """
        if self._duration_ms is None:
            return False
        return self.elapsed_ms >= self._duration_ms

    def update(self):
        """
        Updates the internal time and checks if the timer has ended. If the timer has ended,
        the on_timer_end callback is called, and the timer is either stopped or restarted
        based on the one_shot setting.
        """
        if not self._is_running:
            return
        if self.has_ended:
            if callable(self._on_timer_end):
                self._on_timer_end()
            if self._one_shot:
                self.stop()
            else:
                self.restart()