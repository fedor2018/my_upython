from pyb import Pin, Timer

def startV():
    """ freq 1khz for voltage -V """
    p = Pin('A8')
    tim = Timer(1 , freq=1000)
    ch = tim.channel(1, Timer.PWM, pin=p)
    ch.pulse_width_percent(50)
