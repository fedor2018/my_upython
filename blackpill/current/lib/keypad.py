from pyb import ExtInt, Pin
import time

class keypad:
    def __init__(self):
        self.press=False
        self.x1=Pin("A0", Pin.OUT_OD)
        self.x2=Pin("A1", Pin.OUT_OD) #!!!!
        self.x3=Pin("A2", Pin.OUT_OD)
        self.x4=Pin("A3", Pin.OUT_OD)

        self.p1=Pin("B5", Pin.IN)
        self.p2=Pin("B4", Pin.IN)
        self.p3=Pin("B3", Pin.IN)
        self.p4=Pin("A15", Pin.IN)

        self.y1=ExtInt("B5", ExtInt.IRQ_RISING_FALLING, Pin.PULL_NONE, self.key_press)
        self.y2=ExtInt("B4", ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, self.key_press)
        self.y3=ExtInt("B3", ExtInt.IRQ_RISING_FALLING, Pin.PULL_NONE, self.key_press)
        self.y4=ExtInt("A15", ExtInt.IRQ_RISING_FALLING, Pin.PULL_NONE, self.key_press)

        self.y=[self.p1, self.p2, self.p3, self.p4]
        self.e=[self.y1, self.y2, self.y3, self.y4]
        self.x=[self.x1, self.x2, self.x3, self.x4]

    def key_press(self, l):
        print(l)
#         self.scan()
        
    def setout(self, val):
        for i in range(0,3):
            self.x[i].value(val)
            if(val==0):
                self.e[i].disable
            else:
                self.e[i].enable
        
    def scan(self):
        self.setout(1)
        for i in range(0,4):
            self.x[i].value(0)
            print("%d: " %i, end="")
            for r in range(0,4):
                print(self.y[r].value(), end="")
            print("")
            self.x[i].value(1)
        self.setout(0)
            
    def row_press(self):
        if(not(self.p1.value() & self.p2.value() & self.p3.value() & self.p4.value())):
           print(self.p1.value(),self.p2.value(),self.p3.value(),self.p4.value())
           self.p1.value(0)
           print(self.p1.value(),self.p2.value(),self.p3.value(),self.p4.value())


