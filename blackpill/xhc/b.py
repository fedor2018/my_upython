# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import pyb
#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
u=pyb.Switch()
if(u):
    pyb.usb_mode('CDC')
else:
    pyb.usb_mode('CDC+MSC')   
print("start")
print(pyb.usb_mode())
# can run arbitrary Python, but best to keep it minimal

import pyb
#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
u = Pin('C13', Pin.IN, Pin.PULL_UP)
# u=pyb.Switch()
if(u.value()):
    pyb.usb_mode('CDC+MSC')
else:
    pyb.usb_mode('CDC+MSC')   
print("start")
print(pyb.usb_mode())
