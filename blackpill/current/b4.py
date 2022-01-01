from pyb import ExtInt, Pin, delay


def key_press(line):
    print(line)

b4p=Pin("B4", Pin.IN)
b4=ExtInt("B4", ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, key_press)

print(b4p.names(),b4p.pin(), b4p.value())

while 1:
    print(b4p.names(),b4p.pin(), b4p.value())
    delay(1000)
    b4.swint()

