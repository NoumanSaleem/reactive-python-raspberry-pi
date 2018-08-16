import time
import datetime
import pygame
import RPi.GPIO as GPIO
import padUtils
from rx import Observable

SWITCH_PIN = 23
KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"]
]
ROW_PINS = [26, 19, 13, 6]
COL_PINS = [5, 11, 9]

pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound("countdown.wav")

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    padUtils.setupPins(ROW_PINS, COL_PINS)

    switchStream = Observable.create(lambda observer: GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=lambda p: observer.on_next(p), bouncetime=50))\
        .map(GPIO.input)

    keypadStream = Observable.create(padUtils.pushKeyPadPress(ROW_PINS))\
        .map(padUtils.getPressedKey(ROW_PINS, COL_PINS, KEYPAD))

    keypadStream.with_latest_from(switchStream, lambda x, y: (x, y))\
        .filter(lambda k: k[1] == GPIO.LOW and k[0] == (datetime.datetime.today().weekday() +1))\
        .throttle_first(sound.get_length() * 1000)\
        .subscribe(lambda k: sound.play())

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Goodbye")
finally:
    GPIO.cleanup()

