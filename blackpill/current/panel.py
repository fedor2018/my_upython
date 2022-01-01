from grblcontrol import *
import time
from  rotary_irq_pyb import RotaryIRQ
import utime
from pyb import ExtInt, Pin
from mkey import keymatrix
import sys

kmap=[["0x18","0x85","$X",""],\
     ["$H","","",""],\
     ["G10P0L20X0","G10P0L20Y0","G10P0L20Z0",""],\
     ["","","",""]]

k=keymatrix(enable_int=False,key_map=kmap)
old_x=0
abs_x=0
p=grblcontrol(debug=False, i2c_port=1)

def x_enc():
    global old_x, abs_x
    val=enc_x.value()
    d=val-old_x
    if(d<=-99 and val<old_x):
        d+=100
    elif(d>=99 and val>old_x):
        d-=100
    elif(d>0 and val<old_x):
        d+=100
        
#     if(d==99):d=-1
#     elif(d==-99):d=1
    if(d):
        g="$J=G21G91F1000X"+str(d*0.01)
        abs_x+=d
        print(f"step: {val},{old_x},{d},{g},{abs_x}")
        p.send(g)
        old_x=val
    pass

enc_x = RotaryIRQ("B12", "B10",
                     pull_up=True,
                     half_step=False,
                     min_val=0, 
                     max_val=99, 
                     reverse=True,
                     range_mode=RotaryIRQ.RANGE_WRAP)
enc_x.add_listener(x_enc)

try:
    p.connect()
    tstep=0
    while 1:
        key=k.key_scan()
        if(key):
           print("key=",key)
           p.send(key)
        tstep+=1
        if(tstep>(100/10)):
            p.upd_stat()
            tstep=0
        time.sleep_ms(10)
except Exception as e:
    print(e)
    sys.print_exception(e)
    p.__del__()
