# can run arbitrary Python, but best to keep it minimal

import pyb
#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
hid_desc = bytes([
    0x06,0x00,0xFF, 	# Usage Page (Vendor-Defined 1) */						
    0x09,0x01, 			# Usage (Vendor-Defined 1) */								
    0xA1,0x01, 			# Collection (Application) */ 									
    0x85,0x04, 				# Report ID (4) */								
    0x09,0x01, 				# Usage (Vendor-Defined 1) */ 								
    0x15,0x00, 				# Logical Minimum (0) */ 									
    0x26,0xFF,0x00, 		        # Logical Maximum (255) */ 									
    0x95,0x05, 				# Report Count (5) */ 										
    0x75,0x08, 				# Report Size (8) */ 										
    0x81,0x02, 				# Input (Data,Var,Abs,NWrp,Lin,Pref,NNul,Bit) */				
    0xC0, 			# End Collection */ 	
    0x06,0x00,0xFF, 	        # Usage Page (Vendor-Defined 1) */ 								
    0x09,0x01, 			# Usage (Vendor-Defined 1) */ 									
    0xA1,0x01, 			# Collection (Application) */ 									
    0x85,0x06, 				# Report ID (6) */ 											
    0x09,0x01, 				# Usage (Vendor-Defined 1) */ 								
    0x15,0x00, 				# Logical Minimum (0) */ 									
    0x26,0xFF,0x00, 		        # Logical Maximum (255) */ 									
    0x95,0x07, 				# Report Count (7) */ 										
    0x75,0x08, 				# Report Size (8) */ 										
    0xB1,0x06, 				# Feature (Data,Var,Rel,NWrp,Lin,Pref,NNul,NVol,Bit) */ 		
    0xC0, 			# End Collection */ 
])

existing_keyboard = list(pyb.hid_keyboard)
existing_keyboard[-1] = hid_desc
hid_new = tuple(existing_keyboard)

u = pyb.Pin('C13', pyb.Pin.IN, pyb.Pin.PULL_UP)
# u=pyb.Switch()
print(u.value())
if(u.value()):
    pass
    r=pyb.usb_mode('CDC+HID', vid=0x10ce, pid=0xeb70, hid=(0, 0, 0, 0x40, hid_desc))
    #PID, subclass, protocol, max_packet_len, report_desc.
else:
    pyb.usb_mode('CDC+MSC')   
print("start")
print(pyb.usb_mode())
