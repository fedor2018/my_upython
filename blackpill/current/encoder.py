from  rotary_irq_pyb import RotaryIRQ
import utime
from pyb import ExtInt, Pin

def pkey(line):
    print("line=",line);

enc_menu = RotaryIRQ("B1", "B0",
                     pull_up=True,
                     half_step=False,
                     min_val=0, 
                     max_val=24, 
                     reverse=True,
                     range_mode=RotaryIRQ.RANGE_WRAP)
enc_menu.add_listener(lambda: print(enc_menu.value()))

key_menu=ExtInt("B2", ExtInt.IRQ_RISING_FALLING,
             Pin.PULL_UP,
                pkey)

enc_x = RotaryIRQ("B12", "B10",
                     pull_up=True,
                     half_step=False,
                     min_val=0, 
                     max_val=99, 
                     reverse=True,
                     range_mode=RotaryIRQ.RANGE_WRAP)
enc_x.add_listener(lambda: print(enc_x.value()))

while 1:
    pass

