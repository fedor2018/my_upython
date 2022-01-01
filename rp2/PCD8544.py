#  PCD8544.py

from machine import Pin, SPI, SoftSPI
from array import array
import time

class PCD8544():
    def __init__(self, spi_id=None, rst=None, ce=None, dc=None, din=None, clk=None):
        self._rst = Pin(rst, Pin.OUT) if rst else None # 14
        self._ce = Pin(ce, Pin.OUT) if ce else ce   # 13
        if self._ce: self.ce(1)
        self._dc = Pin(dc, Pin.OUT) if dc else dc   # 12
        self._dc.high()
        
        self._row = 0
        self._col = 0
        self._x = 0
        self._y = 0
        self.clear()
        if spi_id is not None:
            self._spi = SPI(spi_id, baudrate=1000000, polarity=1, phase=0,
                            sck=Pin(clk), mosi=Pin(din), miso=None)
#         else:
#             self._spi = SoftSPI(baudrate=1000000, polarity=1, phase=0,
#                             sck=Pin(clk), mosi=Pin(din), miso=None)

    def ce(self, l=0):
        if self._ce:
            self._ce.value(l)

    def command(self,c):
        b = bytearray(1)
        b[0] = c
        self._dc.low()
        self.ce(0)
        self._spi.write(b)     # write 1 byte on MOSI
        self.ce(1)


    def data(self, data):
        b = bytearray(1)
        b[0] = c
        self._dc.high()
        self.ce(0)
        self._spi.write(b)     # write 1 byte on MOSI
        self.ce(1)
        
    def reset(self):
        if self._rst:
            self._rst.low()
            time.sleep_ms(50)        # sleep for 50 milliseconds
            self._rst.high()

    # begin
    def begin(self):
        self.reset()
        self.command(0x21)	# extended command
        self.command(0xB1)	# set contrast
        self.command(0x13)	# bias
        self.command(0x04)	# temp coeff
        self.command(0x20)	# normal moded._x
        self.command(0x0C)	# not inverted
        self.display()

    # display
    def display(self):
        self.command(0x40)
        self.command(0x80)
        self._dc.high()
        self.ce(0)
        self._spi.write(self._buf)
        self.ce(1)
        
    def p_char(self, ch):
        fp = (ord(ch)-0x20) * 5
        char_buf = array('b',[0,0,0,0,0])
        f = open('font5x7.fnt','rb')
        f.seek(fp)
        char_buf = f.read(5)
        bp = 84*self._row + 6*self._col
        for x in range (0,5):
            self._buf[bp+x] = char_buf[x]
            self._buf[bp+5] = 0 # put in inter char space
        self._col += 1
        if (self._col>13):
            self._col = 0
            self._row += 1
            if (self._row>5):
                self._row = 0

    def p_string(self, str):
        for ch in (str):
            self.p_char(ch)

    def clear(self):
        self._buf= bytearray(84 * int(48 / 8))
        self._row = 0
        self._col = 0
                
    def pixel(self,x,y,fill):
        r = int(y/8)
        i = r * 84 + x
        b = y % 8
        self._buf[i] = self._buf[i] | ( 1 << b )
        
