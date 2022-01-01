from machine import ADC, Pin

R0=65000
T0=20
B=3950.0

def in_volt(adc):
    return adc.read_u16()*(3.3/65535)

def in_r(adc):
    return R0 / (65535/adc.read_u16() - 1)
    
def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3950.0):
    import math
    steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta
    steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
    steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
    return steinhart

adc0 = ADC(Pin(26))     # create ADC object on ADC pin
adc1 = ADC(Pin(27))     # create ADC object on ADC pin

print ("{} V".format(in_volt(adc0)))
print ("{} V".format(in_volt(adc1)))

print("{} ohm".format( in_r(adc0)))
print("{} ohm".format(in_r(adc1)))

print("{} C".format(steinhart_temperature_C(in_r(adc0), Ro=R0, To=T0, beta=B)))
print("{} C".format(steinhart_temperature_C(in_r(adc1), Ro=R0, To=T0, beta=B)))




