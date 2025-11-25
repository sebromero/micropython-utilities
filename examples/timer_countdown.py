from micropython_utilities import Timer

countdown = 10

def update_countdown():
    global countdown
    if countdown > 0:
        countdown -= 1
        print(f"Countdown: {countdown} seconds remaining")

t1 = Timer(1000, False) # 1 second interval
t1.on_timer_end =update_countdown
t1.start()

while True:
    t1.update()
    if countdown == 0:
        print("Countdown finished!")
        break
