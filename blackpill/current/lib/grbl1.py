from pyb import UART
import time
import re

class grbl():
    def __init__(self, port=1, baudrate=115200):
        #each rocket has (x,y) position; user or calling function has choice
        #of passing in x and y values, or by default they are set at 0
        self.connectstatus = False
        self.port = port
        self.serial_handle = None
        self.baudrate = baudrate
        
    def Connect(self):
        if self.connectstatus == False:
            self.serial_handle = UART(self.port,self.baudrate)
            self.serial_handle.write('\r')
            time.sleep_ms(1)
            s=self.serial_handle.read()
            if(s is not None):
                print(s.decode().strip())
                self.connectstatus = True
                print("Connected to GRBL device")
            else:
                self.connectstatus = False
                print("Timeout from GRBL device")
        else:
            print("GRBL device already connected")
        return self.serial_handle

    def Disconnect(self):
        if self.connectstatus == True:
            print("Now Moving back to origin")
            self.BacktoOrigin()
            self.WaitMoving()
            print("Done")
            self.serial_handle.close()
            self.connectstatus = False
            print("GRBL device disconnected")
        else:
            print("Device not Connected")
        return True

    def ResetGRBL(self): #This is only a software reset, cannot reset when limit switches are hitten.
        self.serial_handle.read()
        self.serial_handle.write(b"$RST=$\n")
        grbl_out = self.serial_handle.readline()
        print(grbl_out)
        if grbl_out == b'[MSG:Restoring defaults]\r\n':
            return True
        else:
            return False
        
    def MoveTo(self,x,y):
        self.serial_handle.read()
        g = GCodeRapidMove(X=x,Y=y)
        self.serial_handle.write(str.encode(str(g)+"\n"))
        grbl_out = self.serial_handle.readline()
        if grbl_out == b'ok\r\n':
            return True
        else:
            return False

    def BacktoOrigin(self):
        self.MoveTo(0,0)
        
    def MoveTo_Block(self,x,y):
        self.serial_handle.read()
        g = GCodeRapidMove(X=x,Y=y)
        self.serial_handle.write(str.encode(str(g)+"\n"))
        grbl_out = self.serial_handle.readline()
        self.WaitMoving()
        if grbl_out == b'ok\r\n':
            return True
        else:
            return False

    def BacktoOrigin_Block(self):
        self.MoveTo(0,0)
        self.WaitMoving()

    def WaitMoving(self):
        runningstatus = "Run"
        while(runningstatus != "Idle"):
            time.sleep(.500)
            runningstatus,xpos,ypos = self.StatusRequest()
            #print(runningstatus,xpos,ypos)
        return True

    def StatusRequest(self):
        if self.connectstatus == False:
            return None
        self.serial_handle.read()
        self.serial_handle.write(b"?")
        time.sleep_ms(10)
        grbl_out = self.serial_handle.readline().decode().strip("<>\n\r")
        print(grbl_out)
        tmp = grbl_out.split("|")
        stat={}
        if len(tmp)>1:
            stat['state']=tmp[0]
            for i in range(1,len(tmp)):
                t=tmp[i].split(":")
                stat[t[0]]=t[1]
        return stat

    # A register dictionary will be returned as the result
    def RegisterRequest(self):
        self.serial_handle.read()
        self.serial_handle.write(b"$$\n")
        regout = {}
        for i in range(34):
            time.sleep_ms(1)
            tmp = self.serial_handle.readline().decode().strip()
            print(tmp)
            tmp2 = tmp.split("=")
            tmp3 = int(tmp2[0].split("$")[-1])
            tmp4 = float(tmp2[1].split("\\")[0])
            result = [tmp3,tmp4]
            regout[tmp3] = tmp4
        print(regout)
        return regout

    def ChangeReg(self,regadd,regval):
        self.serial_handle.read()
        string = "$"+ str(regadd) + "=" + str(regval) + "\n"
        print(string)
        self.serial_handle.write(str.encode(string))
        grbl_out = self.serial_handle.readline()
        if grbl_out == b'ok\r\n':
            return True
        else:
            return False
