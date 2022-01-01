from keypad import *
from pyb import delay
import time

k=keypad()
k.row_press()
print(k.y[0].value())

while 1:
#     time.sleep_ms(500)
    pass
