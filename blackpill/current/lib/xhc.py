import pyb

class xhc:
    """ """
    def __init__(self):
        self.hid = pyb.USB_HID()
        self.rd_buf=bytearray(42)
        pass
    
    def send(self):
        pass
    
    def read(self):
        n=self.hid.recv(self.rd_buf)
        print(n)
        print(self.rd_buf)
#         if(n and rd_buf[0:3]==0xfdfe):
#             print 'rcv'
        pass


    