from pyb import UART
import uasyncio as asyncio
import time

class grbl:
    def __init__(self, port=1, baudrate=115200, debug=False):
        self.debug=debug
        self.uart=UART(port, baudrate, timeout=2 )
        self.dbgmsg(self.uart)
        self.status={}
        self.status['cnt']=0
        self.status['error']=0
        self.status['alarm']=0
        self.status['msg']=""
        self.status['Ov']=[]
        self.status['WPos']=[]
        self.status['MPos']=[]
        self.status['WCO']=[]
        self.status['FS']=[]
        self.status['Pn']=[]
#         self.status['Pn']=['X','Y','Z','P','S']
        self.req_parse(b'\x18' , 1)
        self.req_parse(b"$I\r", 30)
        
    def getstat(self):
        return self.status

    def disconnect(self):
        """ """
        while(self.uart.any()):
            self.uart.read() # flush rx buffer
        print("uart disconnect")
        self.uart.deinit()
        
        
    def __del__(self):
        self.disconnect()   

    def dbgmsg(self, m):
        """ print message if debug """
        if(self.debug):
            print(m)

    def send(self,c):
        self.uart.write(c)

    @micropython.native        
    def send_read(self, c, t=1):
        """ send cmd and wait responce """
        t0=time.time_ns()
        while(self.uart.any()):
            self.uart.read() # flush rx buffer
        self.uart.write(c)
        self.dbgmsg("\nsend: %s" % c)
        time.sleep_ms(t)
        s=None
        while(self.uart.any()):
            time.sleep_ms(1)
            s=self.uart.read()
#             print("rr: " % s)
        self.dbgmsg("delay: %dms" % ((time.time_ns()-t0)/1000000))
        if(s is None):
            return ""
        else:
            self.dbgmsg("read: %s" % s)
            return bytes(x if x <127 else 0x20 for x in s).decode("utf-8").strip("\r\n ")

    def is_connect(self):
        """ check connect """
        s=self.send_read(b"\r")
        if(s == 'ok'):
            print("connect")
            return True
        elif(s == ""):
            print("timeout")
        else:
            print("error: %s" % s)
        return False
    
    @micropython.native        
    def req_parse(self, c, t=1):
        """ """
        s=self.send_read(c, t)
        self.dbgmsg("r: %s" % s)
        try:
            if s.startswith('error:'):
                self.status['error'] = s.split(':')[1]
            elif s == 'ok':
                self.status['ok']=1
            elif 'Grbl' in s:
                self.status['grbl']=s.split(' ')[1]
            elif s.startswith('[VER'):
                self.status["ver"]= s.split(':')[1]
            elif s.startswith('<'):
                params = s.replace('<', '').replace('>', '').split('|')
                self.status['mode'] = params[0]

                for param in params[1:]:
                    k, v = param.split(':')
                    if ',' in v:
                        v = v.split(',')
                        for i, item in enumerate(v):
                            try:
                                v[i] = float(item)
                            except:
                                pass
                        self.status[k] = v
            elif 'ALARM' in s:
                self.status['alarm'] = line.split(':')[1]
            elif s.startswith('[MSG:'):
                self.status['msg']=s.replace('[MSG:', '').replace(']', '')
            else:
                print("ignore: ", s)
            self.status['cnt']+=1
            self.dbgmsg("status={}".format(self.status))
        except:
            print("except: %s" % s)
        return self.status

# async def sender():
#     swriter = asyncio.StreamWriter(uart, {})
#     while True:
#         await swriter.awrite('Hello uart\n')
#         await asyncio.sleep(2)
# 
# async def receiver():
#     sreader = asyncio.StreamReader(uart)
#     while True:
#         res = await sreader.readline()
#         print('Recieved', res)
# 
# loop = asyncio.get_event_loop()
# loop.create_task(sender())
# loop.create_task(receiver())
# loop.run_forever()
# 
