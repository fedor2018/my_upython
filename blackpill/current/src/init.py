from pyb import Pin
from pyb import SPI
from pyb import ExtInt
from pyb import I2C, delay, millis
from grbl import grbl    
from pyb_i2c_lcd import I2cLcd
import upymenu

# from  rotary_irq_pyb import RotaryIRQ
# from lcd_api import LcdApi
# import st7920 

# def test_key():
#     print("press key")

# enc_menu = RotaryIRQ("B0", "B1", pull_up=True, half_step=True)
# enc_x= RotaryIRQ("C14", "C15", pull_up=True, half_step=True)
# enc_z= RotaryIRQ("B9", "B8", pull_up=True, half_step=True)

# print(enc_menu.value())
# print(pyb.Pin.board)

# key_menu=Pin("B2", Pin.IN, Pin.PULL_UP)
# key_menu=ExtInt("B2", ExtInt.IRQ_RISING_FALLING,
#             Pin.PULL_NONE,
#             test_key)

DEFAULT_I2C_ADDR = 0x27
i2c = I2C(1, I2C.MASTER)
if i2c.is_ready(DEFAULT_I2C_ADDR):
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 4, 20)
else:
    print("i2c=0x%x device not found. Scan.." % DEFAULT_I2C_ADDR)
    i2c.scan()
    print ("end scan")

lcd.putstr("helo world 1\n")
lcd.putstr("helo world 2")

# spi=SPI(2, SPI.CONTROLLER, baudrate=1800000)
# screen = st7920.Screen( spi=spi )
g=grbl()
# print("1")
g.Connect()
s=g.StatusRequest()
# print(s['state'])
# g.RegisterRequest()
# g.Disconnect()
#pyb.usb_mode(None)
#pyb.repl_uart(uart)
print("end")
lcd.backlight_off()
