from pyb import Pin, Timer

p = Pin('A8') # X1 has TIM2, CH1
tim = Timer(1 , freq=1000)
ch = tim.channel(1, Timer.PWM, pin=p)
ch.pulse_width_percent(50)

from pyb import I2C, delay, millis
from pyb_i2c_lcd import I2cLcd

i2c = I2C(1, I2C.MASTER)
lcd = I2cLcd(i2c, 0x27, 4, 20)
lcd.putstr("HELLO")    

print("start")

while 1:
    pass

