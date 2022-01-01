from grbl import *
from pyb import I2C, delay, millis
from pyb_i2c_lcd import I2cLcd
from lcd_v_minus import *
import time
"""
        X
01234567890123456789
X=-xxx.xx F=xxxx*  W
Y=-xxx.xx S=xxxx* FM
Z=-xxx.xx Idle. XYZP
message
---------------------
* override
F - feed
S - spindle
W - coordinate W M O
FM - flood mist
xyzp - pins
"""
"""
<Idle|  #Idle, Run, Hold, Jog, Alarm, Door, Check, Home, Sleep
MPos:0.000,0.000,0.000| #machine position !WPos = MPos - WCO
WPos:0.000,0.000,0.000| #work position    !MPos = WPos + WCO
WCO:0.000,0.000,0.000|  #Work Coordinate Offset
Bf:15,128| #Buffer
Ln:99999| #line number
FS:0,1000| #Current Feed and Speed
Ov:100,100,100| #Override % feed, rapids, and spindle 
A:SFM| # SC - spindle, F flood, M mist ON
Pn:XYZPDHRS | #Input Pin State
ALARM:5
MSG:
error:
"""
class grblcontrol:
    """ """
    def __init__(self, debug=False, uart_port=1, baudrate=115200, i2c_port=1, i2c_addr=0x27):
        self.ver='20211206'
        self.debug=debug
        self.g=grbl(uart_port,baudrate,debug)
        startV()
        i2c = I2C(i2c_port, I2C.MASTER)
        if not i2c.is_ready(i2c_addr):
            print("i2c port=%d device 0x%x not found. Scan.." % (i2c_port, i2c_addr))
            i2c.scan()
            print ("end scan")
            raise "lcd not found"
        self.lcd = I2cLcd(i2c, i2c_addr, 4, 20)
        self.lcd.backlight_on()

    def __del__(self):
        self.lcd.backlight_off()

    def tstart(self):
        if(self.debug):
            self.t0=time.time_ns()

    def tstop(self):
        if(self.debug):
            print("delay: %dms" % ((time.time_ns()-self.t0)/1000000))

    def xy(self, x=0, y=0):
        self.lcd.move_to(x,y)
        
    def lcdprint(self, str=""):
        self.lcd.putstr(str)

    def connect(self):
        self.lcd.clear()
        self.xy(1,0)
        self.lcdprint("panel ver.%s" % self.ver)
        self.xy(1,1)
        s=self.g.getstat()
        self.lcdprint("grbl %s" % s['ver'])
#         print(s['ver'])
        self.xy(1,2)
        if(self.g.is_connect()):
            self.lcdprint("connected")
        else:
            self.lcdprint("error")
        time.sleep_ms(1000)
        self.lcd.clear()
        self.lcdstatic()

    def lcdstatic(self):
        self.xy()
        self.lcdprint("X=")
        self.xy(0,1)
        self.lcdprint("Y=")
        self.xy(0,2)
        self.lcdprint("Z=")
        self.xy(10,0)
        self.lcdprint("F=")
        self.xy(10,1)
        self.lcdprint("S=")

    def send(self,c):
        self.g.send_read(c+"\r\n")

    @micropython.native        
    def upd_stat(self):
        self.tstart()
        s=self.g.req_parse(b'?')
        if('WPos' in s):
            self.xy(19,0)
            self.lcdprint("W")
        for i in range(0,3): ## pos
            self.xy(2,i)
            self.lcdprint("{: 7.2f}".format(s['WPos'][i]))
        self.xy(12, 0) # feed
        self.lcdprint("{:>4}".format(s['FS'][0]))
        try:
#             if(s['Ov'][0] != 100.0): #feed
                self.lcdprint("*")
        except KeyError:
            self.lcdprint(" ")
        self.xy(12, 1) # spindle
        self.lcdprint("{:>4}".format(s['FS'][1]))
        try:
#             if(s['Ov'][2] != 100.0): #speed
                self.lcdprint("*")
        except KeyError:
            self.lcdprint(" ")
        self.xy(10,2) # mode
        self.lcdprint("{:<5}".format(s['mode']))
        self.xy(16,2)
        self.lcdprint("{:$>}".format(''.join(s['Pn'][0:4])))
        self.xy(0,3) # messages
        str=""
        if(s['error']):
            str+="err:%d " % s['error']
        if(s['alarm']):
            str+="alarm:%d " % s['alarm']
        if(s['msg']):
            str+=s['msg']
        self.lcdprint("{:<20}".format(str))
        self.tstop()
