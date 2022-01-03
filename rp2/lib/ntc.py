from machine import ADC, Pin
from math import log

class NTC():
    """ """
    def __init__(self, adc=None, Vref=3.3, R=10000, Ro=10000.0, To=25.0, beta=3950.0, V=5 ):
        self._adc=adc
        self._vref=Vref
        self._r=R
        self._v=V
        self._r0=Ro
        self._t0=To
        self._beta=beta
        
    def r_UP(self):
        """
        use voltage divider
        Vi--=NTC=--Vo--=R=--GND
        r=(Vi/Vo)*R-R
        """
        return (self._v/self.in_volt())*self._r-self._r

    def r_DN(self):
        """
        use voltage divider
        Vi--=R=--Vo--=NTC=--GND
                
        """
        return self._r / (65535/self._adc.read_u16() - 1)
    
    def in_volt(self):
        return self._adc.read_u16()*(self._vref/65535)
         
    def to_temp(self, r):
        steinhart = log(r / self._r0) / self._beta # log(R/Ro) / beta
        steinhart += 1.0 / (self._t0 + 273.15)          # log(R/Ro) / beta + 1/To
        steinhart = (1.0 / steinhart) - 273.15          # Invert, convert to C
        return steinhart
