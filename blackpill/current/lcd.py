from pyb import I2C, delay, millis
from pyb_i2c_lcd import I2cLcd
from lcd_v_minus import *
 
import time
t1=time.time_ns()

startV()

DEFAULT_I2C_ADDR = 0x27
i2c = I2C(1, I2C.MASTER)
if i2c.is_ready(DEFAULT_I2C_ADDR):
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 4, 20)
else:
    print("i2c=0x%x device not found. Scan.." % DEFAULT_I2C_ADDR)
    i2c.scan()
    print ("end scan")
print((time.time_ns()-t1)/1000000)
lcd.backlight_on()

lcd.move_to(5,1)
lcd.putstr("H E L L O !")
print((time.time_ns()-t1)/1000000)
delay(5000)
lcd.backlight_off()



