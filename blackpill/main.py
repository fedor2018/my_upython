import pyb

if(pyb.usb_mode('CDC+HID')):
    pass
else:
    print('ok')
