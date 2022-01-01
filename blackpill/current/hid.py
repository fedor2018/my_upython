import pyb
from xhc import *

# print(pyb.usb_mode('VCP+HID', hid=pyb.hid_mouse))
# pyb.usb_mode('CDC+HID',hid=pyb.hid_keyboard)
# print(pyb.usb_mode())
# hid = pyb.USB_HID ()
# print(hid)
print(pyb.usb_mode())
# while (1):
# hid.send
x=xhc()
x.read()
