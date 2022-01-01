import st7920
from machine import Pin, SPI
from lcd_v_minus import *

startV()
spi = SPI(2, baudrate=100000) #, polarity=1, phase=1, sck=machine.Pin(18), mosi=machine.Pin(23))

screen = st7920.Screen(spi=spi)

def clear():
    screen.clear()
    screen.redraw()

def draw():

    # write zeroes to the buffer
    screen.clear()

    # draw some points, lines, rectangles, filled rectangles in the buffer
    screen.plot(5, 5) 
    screen.line(10, 10, 15, 15)
    screen.rect(20, 20, 25, 25)
    screen.fill_rect(30, 30, 40, 40)
    screen.fill_rect(32, 32, 38, 38, False)

    # send the buffer to the display
    screen.redraw()

def run():
    clear()
    while 1:
        draw()

if __name__ == "__main__":
    run()
    
