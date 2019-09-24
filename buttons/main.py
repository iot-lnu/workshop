from machine import Pin
import time

button = Pin('P20', mode=Pin.IN, pull=Pin.PULL_UP)

is_pressed = False
 
while True:
    print(button())
    time.sleep(5)
    if button() == 1 and not is_pressed:
        time.sleep(1)
    elif button() == 0 and not is_pressed:
        print("Button pressed")
        is_pressed = True
    elif button() == 1 and is_pressed:
        print("Button released")
        is_pressed = False
    else:
        pass
