import RPi.GPIO as GPIO

def setupPins(rowPins, colPins):
    for pin in rowPins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP);

    for pin in colPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def getPressedKey(rowPins, colPins, keypad):
    def handle(rowChannel):
        rowVal = rowPins.index(rowChannel)
        colVal = None
        for i in range(len(colPins)):
            pin = colPins[i]
            GPIO.output(pin, GPIO.HIGH)
            if (GPIO.input(rowChannel) == GPIO.HIGH):
                GPIO.output(pin, GPIO.LOW)
                colVal = i
                break
            GPIO.output(pin, GPIO.LOW)

        return keypad[rowVal][colVal]
    return handle

def pushKeyPadPress(rowPins, bouncetime=200):
    def handle(observer):
        for pin in rowPins:
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=lambda p: observer.on_next(p), bouncetime=bouncetime)
    return handle
