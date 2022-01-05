from PCD8544 import PCD8544
import lcd_gfx
from ntc import *
import time
from machine import Pin, Timer

led = Pin(25, Pin.OUT, value=1)
# """
r=Pin(10, Pin.OUT, value=0)
IRQ_RISING_FALLING = Pin.IRQ_RISING | Pin.IRQ_FALLING
def mkey(l):
    r.value( 0 if key_menu.value() else 1)
#     print(l)
    print("pin=%d key=%d" % (r.value(), (key_menu.value())))
#     print(key_menu.value())

timer = Timer()
def debounce(pin):
    timer.init(mode=Timer.ONE_SHOT, period=50, callback=mkey)

key_menu=Pin(13, Pin.IN, Pin.PULL_UP)
key_menu.irq(debounce, IRQ_RISING_FALLING)
# """

ntc0=NTC(adc=ADC(Pin(26)), R=3000, Ro=47000, beta=3740, V=3.3)
ntc1=NTC(adc=ADC(Pin(27)), R=3000, Ro=47000, beta=3740, V=3.3)

d = PCD8544(spi_id=0, dc=17, din=19, clk=18, dout=16)
print(d._spi)
# d.begin()
# 
# d.p_string("Start ")
# d.display()
# time.sleep(1)
d.init()
d.LClear()
dot=""
while 1:
    d.LClear()
    d.setxy(0,0)
    d.LPrint ("{:.3f}V".format(ntc0.in_volt()))
    d.setxy(7,0)
    d.LPrint ("{:.3f}V ".format(ntc1.in_volt()))

    r0=ntc0.r_DN()
    d.setxy(0,)
    d.LPrint("{:.2f}K".format(r0/1000)) 
    r1=ntc1.r_DN()
    d.setxy(7,1)
    d.LPrint("{:.2f}K".format(r1/1000))

    d.setxy(0,2)
    d.LPrint("{:.1f}C".format(ntc0.to_temp(ntc0.r_DN())))
    d.setxy(7,2)
    d.LPrint("{:.1f}C".format(ntc1.to_temp(ntc1.r_DN())))

    d.setxy(0,4)
    if len(dot)>=14:
        dot=""
    dot += "."
    d.LPrint(dot)
#    d.display()
    d.setxy(3,3)
    d.LPrint("*" if r.value else ".")

    led.value( 0 if led.value() else 1)
#     print("%d %d" % (r.value(), key_menu.value()))
    time.sleep(1)
