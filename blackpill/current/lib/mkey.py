from machine import Pin
from pyb import ExtInt
import time
# import micropython
# micropython.alloc_emergency_exception_buf(100)

class keymatrix:
    """ """
    def __init__(self, enable_int=True,
                 p_in=["B5", "B4", "B3", "A15"],
                 p_out=["A0", "A1", "A2", "A3"],
                 key_map=None):
        self.row_list=p_out
        self.col_list=p_in
        self.ext_list={}
        for x in range(0,4):
            self.row_list[x]=Pin(p_out[x], Pin.OUT_OD)
            self.row_list[x].value(1)
        for x in range(0,4):
            self.col_list[x]=Pin(p_in[x], Pin.IN, Pin.PULL_UP)
            if(enable_int):
                ext=ExtInt(p_in[x], ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, self.key_press)
                self.ext_list[ext.line()]=x
        if(key_map is None):
            self.key_map=[["D","#","0","*"],\
                     ["C","9","8","7"],\
                     ["B","6","5","4"],\
                     ["A","3","2","1"]]
        else:
            self.key_map=key_map
        self.key_start=0
        self.key=""
#         print("row=",self.row_list)
#         print("col=",self.col_list)
#         print("map=",self.key_map)
        
    def get_key_map(self, r, result):
        return(self.key_map[int(self.row_list.index(r))][int(result.index(0))])

    def key_press(self, pin_on):
#         print("press=",pin_on)
        self.key=pin_on
#         self.key_start=ticks_add(time.ticks_ms(), 100)
#         for r in self.row_list:
#             print(r.value())
#             if r == pin_on:
#                 self.key_start=ticks_add(time.ticks_ms(), 100)
#                 key=self.key_map[int(self.row_list.index(r))][ext_list[pin_on]]
#                 print(key)
#                 return(self.get_key_map(r))

    def key_scan(self):
        for r in self.row_list:
            r.value(0)
            result=[self.col_list[0].value(),
                    self.col_list[1].value(),
                    self.col_list[2].value(),
                    self.col_list[3].value()]
            if min(result)==0:
                r.value(1) # manages key keept pressed
                key=self.key_map[int(self.row_list.index(r))][int(result.index(0))]
#                 print(key, "=", self.key)
                if(self.key!=key):
                    self.key=key
                    return(self.key)
                else:
                    return
            r.value(1)
        self.key=""
        
    def key_bounce(self):
        """ """
        if(self.key_start and ticks_diff(self.key_start,time.ticks_ms())== 0):
            self.key_start=0
            return self.key_scan()


